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
from sandbox.utils.extraction import default_extract_helper, extract_code_from_freeform_completion
from sandbox.utils.sandbox_client import run_code_in_sandbox


def stop_token_trim(s: str, row: Dict[str, Any]) -> str:
    stop_tokens = row['labels'].get('stop_tokens')
    if stop_tokens:
        for st in stop_tokens:
            index = s.find(st)
            if index != -1:
                s = s[:index]
    return s


class HumanEvalDeprecatedDataset(CodingDataset):
    '''
    this class assumes:
    - each dataset has only one language
    - append the raw completion to the code
    '''

    run_lang_map = {
        'humaneval_python': 'python',
        'humaneval_cpp': 'cpp',
        'humaneval_typescript': 'typescript',
        'humaneval_bash': 'bash',
        'humaneval_csharp': 'csharp',
        'humaneval_go': 'go_test',
        'humaneval_java': 'java',
        'shadow_humaneval_python': 'python',
        'humaneval_form_cpp': 'cpp',
        'humaneval_form_go': 'go',
        'humaneval_form_javascript': 'nodejs',
        'humaneval_form_java': 'java',
        'evoeval': 'python',
        'bigcodebench': 'pytest',
    }
    extract_lang_map = {
        'humaneval_python': 'python',
        'humaneval_cpp': 'cpp',
        'humaneval_typescript': 'typescript',
        'humaneval_bash': 'bash',
        'humaneval_csharp': 'csharp',
        'humaneval_go': 'go',
        'humaneval_java': 'java',
        'shadow_humaneval_python': 'python',
        'humaneval_form_cpp': 'cpp',
        'humaneval_form_go': 'go',
        'humaneval_form_javascript': 'nodejs',
        'humaneval_form_java': 'java',
        'evoeval': 'python',
        'bigcodebench': 'python',
    }

    @classmethod
    async def get_prompts(cls, request: GetPromptsRequest) -> List[Prompt]:
        rows = await get_rows_in_table(
            request,
            cls.get_table_name(request.dataset),
            columns=['id', 'labels', 'content'],
        )
        return [cls._generate_single_prompt(r, request.dataset, request.config) for r in rows]

    @classmethod
    async def get_prompt_by_id(cls, request: GetPromptByIdRequest) -> Prompt:
        row = await get_row_by_id_in_table(request,
                                           cls.get_table_name(request.dataset),
                                           columns=['id', 'labels', 'content'])
        return cls._generate_single_prompt(row, request.dataset, request.config)

    @classmethod
    def _generate_single_prompt(cls, row: Dict[str, Any], dataset: str, config: TestConfig) -> Prompt:
        prompt = row['content']
        ensure_json(row, 'labels')
        if config.extra.get('is_freeform'):
            language = cls.extract_lang_map.get(dataset, row['labels'].get('programming_language'))
            locale = config.locale if hasattr(config, 'locale') else 'en'

            if locale == 'zh':
                instruction = f'请按照docstring的要求补全如上代码，写出完整的代码，代码要用markdown语法包裹。'
            else:
                instruction = f'Please complete the above code according to the requirements in the docstring. Write the complete code and wrap it in markdown syntax.'

            prompt = f'```{language}\n{prompt}\n```\n\n{instruction}'

        return Prompt(id=row['id'], prompt=prompt, labels=row['labels'])

    @classmethod
    async def evaluate_single(cls, request: SubmitRequest) -> EvalResult:
        row = await get_row_by_id_in_table(request,
                                           cls.get_table_name(request.dataset),
                                           columns=['id', 'content', 'test', 'labels'])
        ensure_json(row, 'labels')

        is_freeform = bool(request.config.extra.get('is_freeform'))

        if is_freeform:
            if request.dataset in [
                    'humaneval_python', 'humaneval_typescript', 'humaneval_go', 'humaneval_form_go', 'evoeval'
            ] or row['labels'].get('programming_language') == 'go':
                completion, full_code = cls._gen_sft_func_code(request, row)
            else:
                completion, full_code = cls._gen_sft_stop_token_code(request, row)
        else:
            completion, full_code = cls._gen_pretrain_code(request, row)

        if request.dataset in ['humaneval_python', 'shadow_humaneval_python', 'evoeval']:
            full_code = f"{full_code}\ncheck({row['labels']['entry_point']})"
        if request.dataset in ['humaneval_java', 'humaneval_form_java'
                              ] or row['labels'].get('programming_language') == 'java':
            full_code = full_code.replace('class Problem', 'class Main')

        if request.config.run_timeout is None and request.dataset == 'bigcodebench':
            # bigcodebench has large tests
            request.config.run_timeout = 60

        language = cls.run_lang_map.get(request.dataset, row['labels'].get('programming_language'))
        result = await run_code_in_sandbox(
            RunCodeRequest(
                code=full_code,
                language=language,
                compile_timeout=request.config.compile_timeout or 20,
                run_timeout=request.config.run_timeout or 20,
            ))
        accepted = result.status == RunStatus.Success

        return EvalResult(id=request.id,
                          accepted=accepted,
                          extracted_code=completion,
                          full_code=full_code,
                          tests=[EvalTestCase(
                              passed=accepted,
                              exec_info=result,
                          )])

    @classmethod
    def _gen_pretrain_code(cls, request: SubmitRequest, row: Dict[str, Any]) -> str:
        completion = request.completion
        completion = stop_token_trim(completion, row)
        prompt = cls._generate_single_prompt(row, request.dataset, request.config).prompt
        full_code = f"{prompt}\n{completion}\n{row['test']}"
        return completion, full_code

    @classmethod
    def _gen_sft_stop_token_code(cls, request: SubmitRequest, row: Dict[str, Any]) -> str:
        completion = request.completion
        language = cls.extract_lang_map.get(request.dataset, row['labels'].get('programming_language'))
        completion, _ = extract_code_from_freeform_completion(completion, language)
        completion = stop_token_trim(completion, row)
        full_code = f"{completion}\n{row['test']}"
        return completion, full_code

    @classmethod
    def _gen_sft_func_code(cls, request: SubmitRequest, row: Dict[str, Any]) -> str:
        completion = request.completion
        language = cls.extract_lang_map.get(request.dataset, row['labels'].get('programming_language'))
        completion = default_extract_helper(completion, language)
        full_code = f"{completion}\n{row['test']}"
        return completion, full_code
