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
import shlex
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
from sandbox.utils.execution import cleanup_process, ensure_bash_integrity, get_output_non_blocking, kill_process_tree

logger = structlog.stdlib.get_logger()
config = RunConfig.get_instance_sync()


async def run_command_bare(command: str | List[str],
                           timeout: float = 10,
                           stdin: Optional[str] = None,
                           cwd: Optional[str] = None,
                           extra_env: Optional[Dict[str, str]] = {},
                           use_exec: bool = False,
                           preexec_fn=None) -> CommandRunResult:
    try:
        logger.debug(f'running command {command}')
        if use_exec:
            p = await asyncio.create_subprocess_exec(*command,
                                                     stdin=subprocess.PIPE,
                                                     stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE,
                                                     env={
                                                         **os.environ,
                                                         **(extra_env or {})
                                                     },
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
                                                      preexec_fn=preexec_fn)
        if stdin is not None:
            try:
                if p.stdin:
                    p.stdin.write(stdin.encode())
                    p.stdin.flush()
                else:
                    logger.warning("Attempted to write to stdin, but stdin is closed.")
            except Exception as e:
                logger.exception(f"Failed to write to stdin: {e}")
        if p.stdin:
            try:
                p.stdin.close()
            except Exception as e:
                logger.warning(f"Failed to close stdin: {e}")
        start_time = time.time()
        try:
            await asyncio.wait_for(p.wait(), timeout=timeout)
            execution_time = time.time() - start_time
            logger.debug(f'stop running command {command}')
        except asyncio.TimeoutError:
            return CommandRunResult(status=CommandRunStatus.TimeLimitExceeded,
                                    execution_time=time.time() - start_time,
                                    stdout=await get_output_non_blocking(p.stdout),
                                    stderr=await get_output_non_blocking(p.stderr))
        finally:
            if psutil.pid_exists(p.pid):
                kill_process_tree(p.pid)
                logger.info(f'process killed: {p.pid}')
            if config.sandbox.cleanup_process:
                cleanup_process()
            if config.sandbox.restore_bash:
                ensure_bash_integrity()

        return CommandRunResult(status=CommandRunStatus.Finished,
                                execution_time=execution_time,
                                return_code=p.returncode,
                                stdout=await get_output_non_blocking(p.stdout),
                                stderr=await get_output_non_blocking(p.stderr))
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

    elif config.sandbox.isolation == 'foil':
        # foil (https://github.com/ai-agentic-tools/Foil) isolates each command as an ordinary user:
        # system folders read-only, only cwd writable, a private /tmp and home, its own PID and IPC
        # namespaces, no network, a clean environment, and cgroup limits. FOIL names the binary;
        # FOIL_ALLOW_READ (colon-separated) shows extra folders, such as an interpreter outside /usr.
        foil = os.environ.get('FOIL', 'foil')
        reads = [p for p in os.environ.get('FOIL_ALLOW_READ', '').split(':') if p]
        path = (extra_env or {}).get('PATH', os.environ.get('PATH', ''))
        memory = f'{args.memory_limit_MB}M' if args.memory_limit_MB > 0 else '4G'
        flags = ['--strict', '--memory', memory, '--cpus', '1', '--allow-write', cwd, '--setenv', f'PATH={path}']
        for p in reads:
            flags += ['--allow-read', p]

        def wrap(command: str) -> str:
            return f'cd {shlex.quote(cwd)} && exec {shlex.join([foil, "run", *flags, "--", "bash", "-c", command])}'

        if compile_command is not None:
            compile_res = await run_command_bare(wrap(compile_command), args.compile_timeout, None, cwd, extra_env)
        if compile_res is None or (compile_res.status == CommandRunStatus.Finished and compile_res.return_code == 0):
            run_res = await run_command_bare(wrap(run_command), args.run_timeout, args.stdin, cwd, extra_env)
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
