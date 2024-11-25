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

import base64
import json
import re
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
from sandbox.utils.sandbox_client import run_code_in_sandbox


def extract_python_code(completion: str) -> str:
    patterns = {
        'tag': r'\[Python\](.*?)\[/Python\]',
        'tag_with_code': r'\[Python\](.*?)```',
        'tag_without_end': r'\[Python\](.*?)',
        'py_code_block': r'```python[\n\r](.*?)[\n\r]```',
        'generic_code_block': r'```[\n\r](.*?)[\n\r]```',
        'function_def': r'def\s(.*)',
        'class_def': r'class\s(.*)',
        'import_stmt': r'import\s(.*)',
        'from_import': r'from\s(.*)'
    }

    code = 'NaN'
    try:
        if match := re.search(patterns['tag'], completion, re.DOTALL):
            if '```' not in match.group(1):
                code = match.group(1)
            elif '[Python]' in completion and '```python' not in completion:
                code = (re.search(patterns['tag_with_code'], completion, re.DOTALL) or
                        re.search(patterns['tag_without_end'], completion, re.DOTALL)).group(1)
        elif '```python' in completion:
            code = re.search(patterns['py_code_block'], completion, re.DOTALL).group(1)
        elif '```' in completion:
            code = re.search(patterns['generic_code_block'], completion, re.DOTALL).group(1)
        elif all(x in completion for x in ('from ', 'import ')):
            pattern = patterns['from_import'] if completion.find('from') < completion.find(
                'import') else patterns['import_stmt']
            code = re.search(pattern, completion, re.DOTALL).group()
        elif 'import ' in completion:
            code = re.search(patterns['import_stmt'], completion, re.DOTALL).group()
        elif 'from ' in completion:
            code = re.search(patterns['from_import'], completion, re.DOTALL).group()
        elif 'class ' in completion:
            code = re.search(patterns['class_def'], completion, re.DOTALL).group()
        elif 'def ' in completion:
            code = re.search(patterns['function_def'], completion, re.DOTALL).group()
    except Exception:
        pass

    return 'import pytest\n' + code


def extract_java_code(completion: str) -> List[str]:
    patterns = {
        'tag': r'\[Java\](.*?)\[/Java\]',
        'java_code_block': r'```java[\n\r](.*?)[\n\r]```',
        'public_class': r'public\s(.*?)}}',
        'java_code_block_alt': r'```Java(.*?)```',
        'generic_code_block': r'```[\n\r](.*?)[\n\r]```',
        'import_with_end': r'import\s(.*?)}}',
        'class_with_end': r'class\s(.*?)}}',
        'interface_with_end': r'interface\s(.*?)}}'
    }

    code = ['NaN']
    try:
        if '[Java]' in completion:
            code = [re.search(patterns['tag'], completion, re.DOTALL).group(1)]
        elif any(x in completion for x in ('```java', '```Java', '```')):
            code = re.findall(patterns['java_code_block'], completion, re.DOTALL)
            completion = re.sub(r'```java.*?```', '', completion, flags=re.DOTALL)
            code += re.findall(patterns['java_code_block_alt'], completion, re.DOTALL)
            completion = re.sub(r'```Java.*?```', '', completion, flags=re.DOTALL)
            code += re.findall(patterns['generic_code_block'], completion, re.DOTALL)
        elif 'import ' in completion:
            code = [re.search(patterns['import_with_end'], completion, re.DOTALL).group()]
        elif any(x in completion for x in ('public ', 'interface ', 'class ')):
            indices = {k: completion.find(k) for k in ('public ', 'interface ', 'class ')}
            indices = {k: v for k, v in indices.items() if v != -1}
            first = min(indices, key=indices.get)
            pattern = patterns['public_class'] if first == 'public ' else \
                      patterns['interface_with_end'] if first == 'interface ' else \
                      patterns['class_with_end']
            code = [re.search(pattern, completion, re.DOTALL).group()]
    except Exception:
        pass

    return code


def get_java_test_assets(code: List[str], test: str) -> Dict[str, str]:
    files = {}
    patterns = {
        'import': r'(\n|^)(import .*?)\n',
        'interface': r'((@.*?)?(\n[^\n]*)?interface .*?[;}]\s*\n+})',
        'class': r'((@.*?)?(\n[^\n]*)?class .*?[;}]\s*\n+})',
        'enum': r'((@.*?)?(\n[^\n]*)?enum .*?[;}]?\s*\n+})',
        'interface_name': r'interface (.*?)\s',
        'class_name': r'class (.*?)\s',
        'enum_name': r'enum (.*?)\s'
    }

    for c in code + [test]:
        c = '\n' + c
        imports = [i[1] for i in re.findall(patterns['import'], c, re.MULTILINE)]

        for pattern, name_pattern in [('interface', 'interface_name'), ('class', 'class_name'), ('enum', 'enum_name')]:
            for item in re.findall(patterns[pattern], c, re.DOTALL):
                item = item[0]
                name = re.search(patterns[name_pattern], item, re.DOTALL).group(1)
                files[f'{name}.java'] = ("import org.junit.jupiter.api.Test;\n"
                                         "import static org.junit.jupiter.api.Assertions.*;\n" + "\n".join(imports) +
                                         "\n" + item + '\n')

    return {k: base64.b64encode(v.encode('utf-8')).decode('utf-8') for k, v in files.items()}


class NaturalCodeBenchDataset(CodingDataset):

    @classmethod
    async def get_prompts(cls, request: GetPromptsRequest) -> List[Prompt]:
        rows = await get_rows_in_table(
            request,
            cls.get_table_name(request.dataset),
            columns=['id', 'labels', 'content'],
        )
        return [cls._generate_single_prompt(r, request.config) for r in rows]

    @classmethod
    async def get_prompt_by_id(cls, request: GetPromptByIdRequest) -> Prompt:
        row = await get_row_by_id_in_table(request,
                                           cls.get_table_name(request.dataset),
                                           columns=['id', 'labels', 'content'])
        return cls._generate_single_prompt(row, request.config)

    @classmethod
    def _generate_single_prompt(cls, row: Dict[str, Any], config: TestConfig) -> Prompt:
        prompt = row['content']
        return Prompt(id=row['id'], prompt=prompt, labels=ensure_json(row, 'labels'))

    @classmethod
    async def evaluate_single(cls, request: SubmitRequest) -> EvalResult:
        row = await get_row_by_id_in_table(request, cls.get_table_name(request.dataset), columns=['test', 'labels'])
        ensure_json(row, 'labels')
        ensure_json(row, 'test')
        asset = row['test'].get('asset')
        if isinstance(asset, dict):
            asset = asset
        elif isinstance(asset, str):
            asset = json.loads(asset)
        else:
            asset = {}

        lang = 'python' if 'python' in request.dataset else 'java'

        if lang == 'python':
            code = extract_python_code(request.completion)
            full_code = f'import pytest\n\n{code}\n\n{row["test"]["code"]}'
            files = {}
        if lang == 'java':
            codes = extract_java_code(request.completion)
            code = '\n\n'.join(codes)
            files = get_java_test_assets(codes, row["test"]["code"])
            full_code = ''
            for f, c in files.items():
                full_code += f'// {f}\n\n{base64.b64decode(c.encode("utf-8")).decode("utf-8")}\n\n'

        print(
            RunCodeRequest(code=full_code if lang == 'python' else '',
                           language='pytest' if lang == 'python' else 'junit',
                           run_timeout=request.config.run_timeout or 20,
                           files={
                               **asset,
                               **files
                           }).files.keys())
        # this problem requires more time
        default_timeout = 40 if lang == 'python' and request.id == 52 else 20
        result = await run_code_in_sandbox(
            RunCodeRequest(code=full_code if lang == 'python' else '',
                           language='pytest' if lang == 'python' else 'junit',
                           run_timeout=request.config.run_timeout or default_timeout,
                           files={
                               **asset,
                               **files
                           }))
        accepted = result.status == RunStatus.Success

        return EvalResult(id=request.id,
                          accepted=accepted,
                          extracted_code=code,
                          full_code=full_code,
                          tests=[EvalTestCase(
                              passed=accepted,
                              exec_info=result,
                          )])

    @classmethod
    async def get_canonical_solution(cls, dataset: str, id: int) -> str:
        row = await get_row_by_id_in_table(GetPromptByIdRequest(dataset=dataset, config=TestConfig(), id=id),
                                           cls.get_table_name(dataset),
                                           columns=['canonical_solution'])
        return row['canonical_solution']
