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
import os
import shlex
import signal
import sys

import psutil
import pytest

import sandbox.runners.base as runner_base
from sandbox.runners.base import run_command_bare
from sandbox.runners.types import CommandRunStatus

_OUTPUT_CAPTURE_LIMIT = 1024 * 1024


async def _run_with_watchdog(*args, **kwargs):
    return await asyncio.wait_for(run_command_bare(*args, **kwargs), timeout=10)


async def _assert_process_stopped(pid):
    for _ in range(100):
        try:
            if psutil.Process(pid).status() == psutil.STATUS_ZOMBIE:
                return
        except psutil.NoSuchProcess:
            return
        await asyncio.sleep(0.01)

    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    pytest.fail(f'descendant process {pid} is still running')


@pytest.mark.parametrize('stream_name', ['stdout', 'stderr'])
@pytest.mark.parametrize(('output_size', 'expected_size'), [(256 * 1024, 256 * 1024),
                                                            (2 * 1024 * 1024, _OUTPUT_CAPTURE_LIMIT)])
async def test_run_command_bare_drains_large_output_with_bounded_capture(stream_name, output_size, expected_size):
    command = [sys.executable, '-c', f"import sys; sys.{stream_name}.write('x' * {output_size})"]

    result = await _run_with_watchdog(command, timeout=5, use_exec=True)

    assert result.status == CommandRunStatus.Finished
    assert result.return_code == 0
    assert getattr(result, stream_name) == 'x' * expected_size


@pytest.mark.skipif(os.name != 'posix', reason='shell quoting is POSIX-specific')
async def test_run_command_bare_drains_large_shell_output():
    script = f"import sys; sys.stdout.write('x' * {2 * _OUTPUT_CAPTURE_LIMIT})"
    command = f'{shlex.quote(sys.executable)} -c {shlex.quote(script)}'

    result = await _run_with_watchdog(command, timeout=5)

    assert result.status == CommandRunStatus.Finished
    assert result.return_code == 0
    assert result.stdout == 'x' * _OUTPUT_CAPTURE_LIMIT


async def test_run_command_bare_preserves_output_on_timeout():
    command = [
        sys.executable,
        '-c',
        ("import sys, time; "
         "sys.stdout.write('stdout before timeout\\n'); sys.stdout.flush(); "
         "sys.stderr.write('stderr before timeout\\n'); sys.stderr.flush(); "
         "time.sleep(30)"),
    ]

    result = await _run_with_watchdog(command, timeout=1, use_exec=True)

    assert result.status == CommandRunStatus.TimeLimitExceeded
    assert result.stdout.splitlines() == ['stdout before timeout']
    assert result.stderr.splitlines() == ['stderr before timeout']


@pytest.mark.skipif(os.name != 'posix', reason='process-group semantics are POSIX-specific')
async def test_run_command_bare_kills_descendant_holding_pipes():
    command = [
        sys.executable,
        '-c',
        ("import subprocess, sys; "
         "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)']); "
         "print(child.pid, flush=True)"),
    ]

    result = await asyncio.wait_for(run_command_bare(command, timeout=1, use_exec=True), timeout=3)

    assert result.status == CommandRunStatus.TimeLimitExceeded
    assert result.execution_time < 3
    await _assert_process_stopped(int(result.stdout.strip()))


@pytest.mark.skipif(os.name != 'posix', reason='process-group semantics are POSIX-specific')
async def test_run_command_bare_kills_descendant_after_parent_finishes():
    command = [
        sys.executable,
        '-c',
        ("import subprocess, sys; "
         "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], "
         "stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); "
         "print(child.pid, flush=True)"),
    ]

    result = await _run_with_watchdog(command, timeout=3, use_exec=True)

    assert result.status == CommandRunStatus.Finished
    await _assert_process_stopped(int(result.stdout.strip()))


async def test_run_command_bare_passes_stdin():
    command = [sys.executable, '-c', 'import sys; sys.stdout.write(sys.stdin.read())']

    result = await _run_with_watchdog(command, stdin='hello from stdin', use_exec=True)

    assert result.status == CommandRunStatus.Finished
    assert result.stdout == 'hello from stdin'


async def test_run_command_bare_does_not_start_process_for_invalid_stdin(monkeypatch):
    process_started = False

    async def create_subprocess(*args, **kwargs):
        nonlocal process_started
        process_started = True

    monkeypatch.setattr(asyncio, 'create_subprocess_exec', create_subprocess)

    result = await run_command_bare([sys.executable], stdin='\ud800', use_exec=True)

    assert result.status == CommandRunStatus.Error
    assert 'surrogates not allowed' in result.stderr
    assert not process_started


async def test_run_command_bare_cleans_up_when_cancelled(monkeypatch):
    processes = []
    original_create_subprocess_exec = asyncio.create_subprocess_exec

    async def create_subprocess(*args, **kwargs):
        process = await original_create_subprocess_exec(*args, **kwargs)
        processes.append(process)
        return process

    monkeypatch.setattr(asyncio, 'create_subprocess_exec', create_subprocess)
    command = [sys.executable, '-c', 'import time; time.sleep(30)']
    run_task = asyncio.create_task(run_command_bare(command, timeout=30, use_exec=True))

    for _ in range(100):
        if processes:
            break
        await asyncio.sleep(0.01)
    assert processes

    run_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await asyncio.wait_for(run_task, timeout=3)

    await asyncio.wait_for(processes[0].wait(), timeout=1)
    assert processes[0].returncode is not None


async def test_terminate_and_reap_preserves_cancellation(monkeypatch):
    child_task = asyncio.create_task(asyncio.sleep(30))
    execution = asyncio.gather(child_task)
    monkeypatch.setattr(runner_base, '_terminate_process', lambda process: None)
    cleanup_task = asyncio.create_task(runner_base._terminate_and_reap(object(), [child_task], execution))
    await asyncio.sleep(0)

    cleanup_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await asyncio.wait_for(cleanup_task, timeout=1)

    assert child_task.cancelled()
