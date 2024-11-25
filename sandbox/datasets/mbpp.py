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
from typing import Any, Dict, List

from sandbox.database import get_row_by_id_in_table, get_rows_in_table
from sandbox.datasets.types import (
    CodingDataset,
    EvalResult,
    EvalTestCase,
    GetPromptByIdRequest,
    GetPromptsRequest,
    Prompt,
    RunCodeRequest,
    RunStatus,
    SubmitRequest,
    TestConfig,
)
from sandbox.utils.common import ensure_json
from sandbox.utils.extraction import default_extract_helper
from sandbox.utils.sandbox_client import run_code_in_sandbox


class MBPPDataset(CodingDataset):

    @classmethod
    async def get_prompts(cls, request: GetPromptsRequest) -> List[Prompt]:
        rows = await get_rows_in_table(
            request,
            cls.get_table_name(request.dataset),
            columns=['id', 'labels', 'content', 'test'],
        )
        return [cls._generate_single_prompt(r, request.config) for r in rows]

    @classmethod
    async def get_prompt_by_id(cls, request: GetPromptByIdRequest) -> Prompt:
        row = await get_row_by_id_in_table(request,
                                           cls.get_table_name(request.dataset),
                                           columns=['id', 'labels', 'content', 'test'])
        return cls._generate_single_prompt(row, request.config)

    @classmethod
    def _generate_single_prompt(cls, row: Dict[str, Any], config: TestConfig) -> Prompt:
        tests = ensure_json(row, 'test')
        test = '\n'.join(tests[:1])
        prompt = f"{row['content']} Your code should satisfy these tests:\n\n{test}"
        return Prompt(id=row['id'], prompt=prompt, labels=ensure_json(row, 'labels'))

    @classmethod
    async def evaluate_single(cls, request: SubmitRequest) -> EvalResult:
        row = await get_row_by_id_in_table(request,
                                           cls.get_table_name(request.dataset),
                                           columns=['id', 'content', 'test', 'labels'])
        ensure_json(row, 'labels')
        tests = ensure_json(row, 'test')
        test = '\n'.join(tests)

        code = default_extract_helper(request.completion, 'python', request.config.custom_extract_logic)
        full_code = f"{code}\n{row['labels']['test_setup_code']}\n{test}"

        result = await run_code_in_sandbox(
            RunCodeRequest(
                code=full_code,
                language='python',
                run_timeout=request.config.run_timeout or 20,
            ))
        accepted = result.status == RunStatus.Success

        return EvalResult(id=request.id,
                          accepted=accepted,
                          extracted_code=code,
                          full_code=full_code,
                          tests=[EvalTestCase(
                              passed=accepted,
                              exec_info=result,
                          )])
