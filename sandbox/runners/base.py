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
import base64
import os
import signal
import subprocess
import time
import traceback
from typing import Dict, List, Optional

import psutil
import structlog
import platform
import resource

from sandbox.configs.run_config import RunConfig
from sandbox.runners.isolation import tmp_cgroup, tmp_netns, tmp_overlayfs
from sandbox.runners.types import CodeRunArgs, CodeRunResult, CommandRunResult, CommandRunStatus
from sandbox.utils.common import set_permissions_recursively
from sandbox.utils.execution import cleanup_process, ensure_bash_integrity, kill_process_tree, try_decode

logger = structlog.stdlib.get_logger()
config = RunConfig.get_instance_sync()

_MAX_CAPTURED_OUTPUT_BYTES = 1024 * 1024
_OUTPUT_READ_CHUNK_BYTES = 64 * 1024
_PROCESS_TERMINATION_TIMEOUT = 1.0


async def _drain_stream(stream: Optional[asyncio.StreamReader], captured: bytearray) -> None:
    if stream is None:
        return

    while chunk := await stream.read(_OUTPUT_READ_CHUNK_BYTES):
        remaining = _MAX_CAPTURED_OUTPUT_BYTES - len(captured)
        if remaining > 0:
            captured.extend(chunk[:remaining])


async def _write_stdin(stream: Optional[asyncio.StreamWriter], stdin: Optional[bytes]) -> None:
    if stream is None:
        return

    try:
        if stdin is not None:
            stream.write(stdin)
            await stream.drain()
    except (BrokenPipeError, ConnectionResetError):
        pass
    finally:
        stream.close()


def _terminate_process(process: asyncio.subprocess.Process) -> None:
    if os.name == 'posix':
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except OSError as e:
            logger.warning(f'failed to kill process group {process.pid}: {e}')

    if process.returncode is None and psutil.pid_exists(process.pid):
        try:
            kill_process_tree(process.pid)
        except Exception as e:
            logger.warning(f'failed to kill process tree {process.pid}: {e}')

    if process.returncode is None:
        try:
            process.kill()
        except OSError as e:
            logger.warning(f'failed to kill process {process.pid}: {e}')


async def _terminate_and_reap(process: asyncio.subprocess.Process, tasks: List[asyncio.Task],
                              execution: asyncio.Future) -> None:
    current_task = asyncio.current_task()
    cancellation_requested = bool(current_task and current_task.cancelling())
    try:
        _terminate_process(process)
        try:
            await asyncio.wait_for(asyncio.shield(execution), timeout=_PROCESS_TERMINATION_TIMEOUT)
        except asyncio.CancelledError:
            cancellation_requested = True
        except Exception:
            pass
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        cleanup = asyncio.gather(*tasks, return_exceptions=True)
        while not cleanup.done():
            try:
                await asyncio.shield(cleanup)
            except asyncio.CancelledError:
                cancellation_requested = True
        cleanup.result()
        if not execution.done():
            execution.cancel()
        try:
            execution.exception()
        except asyncio.CancelledError:
            pass

    if cancellation_requested:
        raise asyncio.CancelledError


async def run_command_bare(command: str | List[str],
                           timeout: float = 10,
                           stdin: Optional[str] = None,
                           cwd: Optional[str] = None,
                           extra_env: Optional[Dict[str, str]] = {},
                           use_exec: bool = False,
                           preexec_fn=None) -> CommandRunResult:
    try:
        logger.debug(f'running command {command}')
        stdin_bytes = stdin.encode() if stdin is not None else None
        if use_exec:
            p = await asyncio.create_subprocess_exec(*command,
                                                     stdin=subprocess.PIPE,
                                                     stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE,
                                                     env={
                                                         **os.environ,
                                                         **(extra_env or {})
                                                     },
                                                     start_new_session=True,
                                                     preexec_fn=preexec_fn)
        else:
            p = await asyncio.create_subprocess_shell(command,
                                                      stdin=subprocess.PIPE,
                                                      stdout=subprocess.PIPE,
                                                      stderr=subprocess.PIPE,
                                                      cwd=cwd,
                                                      executable='/bin/bash',
                                                      env={
                                                          **os.environ,
                                                          **(extra_env or {})
                                                      },
                                                      start_new_session=True,
                                                      preexec_fn=preexec_fn)
        stdout = bytearray()
        stderr = bytearray()
        tasks = [
            asyncio.create_task(_write_stdin(p.stdin, stdin_bytes)),
            asyncio.create_task(_drain_stream(p.stdout, stdout)),
            asyncio.create_task(_drain_stream(p.stderr, stderr)),
            asyncio.create_task(p.wait()),
        ]
        execution = asyncio.gather(*tasks)
        start_time = time.time()
        completed = False
        timed_out = False
        try:
            await asyncio.wait_for(asyncio.shield(execution), timeout=timeout)
            completed = True
            execution_time = time.time() - start_time
            logger.debug(f'stop running command {command}')
        except asyncio.TimeoutError:
            timed_out = True
            execution_time = time.time() - start_time
        finally:
            try:
                if not completed:
                    await _terminate_and_reap(p, tasks, execution)
                else:
                    _terminate_process(p)
            finally:
                if config.sandbox.cleanup_process:
                    cleanup_process()
                if config.sandbox.restore_bash:
                    ensure_bash_integrity()

        if timed_out:
            return CommandRunResult(status=CommandRunStatus.TimeLimitExceeded,
                                    execution_time=execution_time,
                                    stdout=try_decode(bytes(stdout)),
                                    stderr=try_decode(bytes(stderr)))

        return CommandRunResult(status=CommandRunStatus.Finished,
                                execution_time=execution_time,
                                return_code=p.returncode,
                                stdout=try_decode(bytes(stdout)),
                                stderr=try_decode(bytes(stderr)))
    except Exception as e:
        message = f'exception on running command {command}: {e} | {traceback.print_tb(e.__traceback__)}'
        logger.warning(message)
        return CommandRunResult(status=CommandRunStatus.Error, stderr=message)


async def run_commands(compile_command: Optional[str], run_command: str, cwd: str, extra_env: Optional[Dict[str, str]],
                       args: CodeRunArgs, **kwargs) -> CodeRunResult:
    files = {}
    compile_res = None
    run_res = None

    if config.sandbox.isolation == 'none':
        preexec_steps = []
        if kwargs.get('set_uid'):
            set_permissions_recursively(cwd, 0o777)
            preexec_steps.append(lambda: os.setuid(kwargs.get('set_uid')))
        
        # Apply memory limit using resource module
        if args.memory_limit_MB > 0:
            def memory_limit_preexec():
                _, hard_memory_limit_AS = resource.getrlimit(resource.RLIMIT_AS)
                _, hard_memory_limit_DATA = resource.getrlimit(resource.RLIMIT_DATA)
                soft_memory_limit = args.memory_limit_MB * 1024 * 1024
                resource.setrlimit(resource.RLIMIT_AS, (soft_memory_limit, hard_memory_limit_AS))
                resource.setrlimit(resource.RLIMIT_DATA, (soft_memory_limit, hard_memory_limit_DATA))
                if platform.uname().system != "Darwin":
                    _, hard_memory_limit_STACK = resource.getrlimit(resource.RLIMIT_STACK)
                    resource.setrlimit(resource.RLIMIT_STACK, (soft_memory_limit, hard_memory_limit_STACK))
            preexec_steps.insert(0, memory_limit_preexec)
        preexec_fn = lambda: [step() for step in preexec_steps] if preexec_steps else None
        
        if compile_command is not None:
            compile_res = await run_command_bare(compile_command,
                                                 args.compile_timeout,
                                                 None,
                                                 cwd,
                                                 extra_env,
                                                 preexec_fn=preexec_fn)
        if compile_res is None or (compile_res.status == CommandRunStatus.Finished and compile_res.return_code == 0):
            run_res = await run_command_bare(run_command,
                                             args.run_timeout,
                                             args.stdin,
                                             cwd,
                                             extra_env,
                                             preexec_fn=preexec_fn)
        for filename in args.fetch_files:
            fp = os.path.abspath(os.path.join(cwd, filename))
            if os.path.isfile(fp):
                with open(fp, 'rb') as f:
                    content = f.read()
                base64_content = base64.b64encode(content).decode('utf-8')
                files[filename] = base64_content
        return CodeRunResult(compile_result=compile_res, run_result=run_res, files=files)

    elif config.sandbox.isolation == 'lite':
        async with tmp_overlayfs() as root, tmp_cgroup(mem_limit='4G', cpu_limit=1) as cgroups, tmp_netns(
                kwargs.get('netns_no_bridge', False)) as netns:
            prefix = []
            for cg in cgroups:
                prefix += ['cgexec', '-g', cg]
            if not kwargs.get('disable_pid_isolation', False):
                prefix += ['unshare', '--pid', '--fork', '--mount-proc']
            prefix += ['ip', 'netns', 'exec', netns]
            prefix += ['chroot', root]

            if compile_command is not None:
                compile_res = await run_command_bare(prefix + ['bash', '-c', f'cd {cwd} && {compile_command}'],
                                                     args.compile_timeout, None, cwd, extra_env, True)
            if compile_res is None or (compile_res.status == CommandRunStatus.Finished and
                                       compile_res.return_code == 0):
                run_res = await run_command_bare(prefix + ['bash', '-c', f'cd {cwd} && {run_command}'],
                                                 args.run_timeout, args.stdin, cwd, extra_env, True)

            for filename in args.fetch_files:
                fp = os.path.join(root, os.path.abspath(os.path.join(cwd, filename))[1:])
                if os.path.isfile(fp):
                    with open(fp, 'rb') as f:
                        content = f.read()
                    base64_content = base64.b64encode(content).decode('utf-8')
                    files[filename] = base64_content
            return CodeRunResult(compile_result=compile_res, run_result=run_res, files=files)


def restore_files(dir: str, files: Dict[str, Optional[str]]):
    for filename, content in files.items():
        if not isinstance(content, str):
            continue
        if "IGNORE_THIS_FILE" in filename:
            continue
        filepath = os.path.join(dir, filename)
        dirpath = os.path.dirname(filepath)
        os.makedirs(dirpath, exist_ok=True)
        with open(filepath, 'wb') as file:
            file.write(base64.b64decode(content))
