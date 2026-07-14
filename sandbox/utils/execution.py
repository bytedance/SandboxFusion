# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import hashlib
import os
import shutil
import sys
from functools import cache, wraps
from typing import Any, Callable, Coroutine, TypeVar

import psutil
import structlog

from sandbox.configs.run_config import RunConfig

config = RunConfig.get_instance_sync()
logger = structlog.stdlib.get_logger()


def try_decode(s: bytes) -> str:
    try:
        r = s.decode()
    except Exception as e:
        r = f'[DecodeError] {e}'
    return r


async def get_output_non_blocking(fd):
    res = b''
    try:
        # read up to 1MB
        res = await asyncio.wait_for(fd.read(1024 * 1024), timeout=0.0001)
    except asyncio.TimeoutError:
        pass
    return try_decode(res)


def kill_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        parent.kill()
    except Exception as e:
        logger.warn(f'error on killing process tree: {e}') 

def cleanup_process():
    try:
        current_pid = os.getpid()
        root_pid = current_pid
        while True:
            try:
                next_pid = psutil.Process(root_pid).ppid()
                if next_pid <= 1:
                    break
                root_pid = next_pid
            except psutil.NoSuchProcess:
                # 如果找不到父进程 (例如已到达沙箱边界)，就此打住
                logger.warning(f"Could not find parent process for {root_pid}. Stopping tree walk.")
                break
        child_pids = [p.pid for p in psutil.Process(root_pid).children(recursive=True)]
        for process in psutil.process_iter(['pid', 'name']):
            pid = process.pid
            if pid < current_pid:
                continue
            if process.terminal() is not None:
                continue
            if pid in child_pids:
                continue
            cmd = ' '.join(process.cmdline())
            if 'bincore/VBCSCompiler.dll' in cmd:
                continue
            blacklist = ['node', 'python', 'go', 'npm', 'bash', 'dotnet', 'g++', 'test', 'flask', 'sleep']
            if not any([w in cmd.lower() for w in blacklist]):
                continue
            try:
                process.kill()
                logger.info(f'process killed: [{pid}] {cmd}')
            except psutil.NoSuchProcess:
                pass
    except Exception as e:
        logger.warn(f'error on cleaning up processes: {e}')


def file_md5(fn: str) -> str:
    with open(fn, "rb") as file:
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
        file_md5 = hash_md5.hexdigest()
    return file_md5


def ensure_bash_integrity():
    internal_bash = os.path.abspath(os.path.join(__file__, '../../runtime/bin/bash'))
    bash_path = '/bin/bash'
    original_md5 = '23c415748ff840b296d0b93f98649dec'
    try:
        if os.path.exists(bash_path) and file_md5(bash_path) == original_md5:
            return
        logger.warning(f'/bin/bash modified, trying to restore...')
        if not os.path.exists(internal_bash):
            logger.error(f'internal bash not found!')
            sys.exit(1)
        if file_md5(internal_bash) != original_md5:
            logger.error(f'internal bash modified!')
            sys.exit(1)
        shutil.copy2(internal_bash, bash_path)
    except Exception as e:
        logger.error(f"failed to recover the integrity of bash: {e}")
        sys.exit(1)


@cache
def get_tmp_dir() -> str:
    TMP_DIR = '/tmp'
    # TMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../tmp'))
    os.makedirs(TMP_DIR, exist_ok=True)
    logger.info(f'tmp dir: {TMP_DIR}')
    return TMP_DIR


@cache
def get_memory_nodes() -> str:
    return open('/sys/fs/cgroup/cpuset/cpuset.mems').read().strip()


T = TypeVar('T', bound=Callable[..., Coroutine[Any, Any, Any]])


def max_concurrency(limit: int) -> Callable[[T], T]:
    """ Decorator to limit the maximum number of concurrent executions of an async function """
    semaphore = asyncio.Semaphore(limit)

    def decorator(func: T) -> T:

        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with semaphore:
                return await func(*args, **kwargs)

        return wrapper

    return decorator


def find_child_with_least_pid(ppid) -> int | None:
    try:
        processes = []
        for p in psutil.process_iter(['pid', 'ppid']):
            if p.ppid() == ppid:
                processes.append(p)
        if not processes:
            logger.warning(f'no child process found')
            return None

        child_with_least_pid = min(processes, key=lambda p: p.pid)
        return child_with_least_pid.pid
    except psutil.NoSuchProcess:
        logger.warning(f'no process with PPID {ppid} found.')
        return None
    except Exception as e:
        logger.warning(f'failed to find_child_with_least_pid: {e}')
        return None
