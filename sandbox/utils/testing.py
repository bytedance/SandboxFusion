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
from typing import List

import structlog
from fastapi import HTTPException

from sandbox.configs.run_config import RunConfig
from sandbox.datasets.types import EvalTestCase, GeneralStdioTest, RunStatus, TestConfig
from sandbox.runners.types import compile_languages
from sandbox.utils.execution import max_concurrency
from sandbox.utils.sandbox_client import RunCodeRequest, run_code_in_sandbox, run_code_in_sandbox_w_retry

sandbox_config = RunConfig.get_instance_sync()
logger = structlog.stdlib.get_logger()


async def check_auto_test_case(code: str, config: TestConfig) -> EvalTestCase:
    '''
    auto test: run the code and check if the return value is 0
    '''
    result = await run_code_in_sandbox(RunCodeRequest(code=code, language=config.language))
    return EvalTestCase(passed=result.status == RunStatus.Success, exec_info=result)


async def check_stdio_test_case(code: str, case: GeneralStdioTest, config: TestConfig, lower_cmp=True) -> EvalTestCase:
    if config.language in compile_languages:
        result = await run_code_in_sandbox_w_retry(
            RunCodeRequest(code=code,
                           language=config.language,
                           stdin=case.input['stdin'],
                           compile_timeout=config.compile_timeout or 10,
                           run_timeout=config.run_timeout or 10))
    else:
        result = await run_code_in_sandbox_w_retry(
            RunCodeRequest(code=code,
                           language=config.language,
                           stdin=case.input['stdin'],
                           run_timeout=config.run_timeout or 20))
    fail_case = EvalTestCase(passed=False, exec_info=result, test_info=case.model_dump())
    if result.status != 'Success':
        return fail_case
    result_lines = result.run_result.stdout.strip().split('\n')
    expected_lines = case.output['stdout'].strip().split('\n')
    if len(result_lines) - len(expected_lines) == 1 and result_lines[-1] == '':
        result_lines = result_lines[:-1]
    if len(expected_lines) - len(result_lines) == 1 and expected_lines[-1] == '':
        expected_lines = expected_lines[:-1]
    if len(result_lines) != len(expected_lines):
        return fail_case
    for rl, el in zip(result_lines, expected_lines):
        if lower_cmp:
            rl = rl.lower()
            el = el.lower()
        if rl.strip() != el.strip():
            return fail_case
    return EvalTestCase(passed=True, exec_info=result, test_info=case.model_dump())


async def check_stdio_test_cases(code: str,
                                 cases: List[GeneralStdioTest],
                                 config: TestConfig,
                                 lower_cmp=True) -> List[EvalTestCase]:
    result = []
    for case in cases:
        outcome = await check_stdio_test_case(code, case, config, lower_cmp)
        result.append(outcome)
        if not outcome.passed:
            break
    return result


async def check_stdio_test_cases_parallel(code: str,
                                          cases: List[GeneralStdioTest],
                                          config: TestConfig,
                                          lower_cmp=True) -> List[EvalTestCase]:
    result = []
    tasks: List[asyncio.Task[EvalTestCase]] = []

    check_stdio_test_case_limited = check_stdio_test_case
    if sandbox_config.online_judge.max_runner_concurrency > 0:
        check_stdio_test_case_limited = max_concurrency(
            sandbox_config.online_judge.max_runner_concurrency)(check_stdio_test_case)

    for case in cases:
        task = asyncio.create_task(check_stdio_test_case_limited(code, case, config, lower_cmp))
        tasks.append(task)

    for task in tasks:
        try:
            outcome = await task
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Failed to check stdio test case: {e}')
        result.append(outcome)
        if not outcome.passed:
            for remaining_task in tasks:
                if not remaining_task.done():
                    remaining_task.cancel()
            break

    return result
