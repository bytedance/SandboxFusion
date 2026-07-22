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

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class CommandRunStatus(str, Enum):
    Finished = 'Finished'
    Error = 'Error'
    TimeLimitExceeded = 'TimeLimitExceeded'


class CommandRunResult(BaseModel):
    status: CommandRunStatus
    execution_time: Optional[float] = None
    return_code: Optional[int] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None


class CodeRunArgs(BaseModel):
    code: str
    files: Dict[str, Optional[str]] = {}
    compile_timeout: float = 10
    run_timeout: float = 10
    memory_limit_MB: int = -1
    stdin: Optional[str] = None
    fetch_files: List[str] = []
    args: List[str] = Field([], description='additional command-line arguments passed to pytest')


class CodeRunResult(BaseModel):
    compile_result: Optional[CommandRunResult] = None
    run_result: Optional[CommandRunResult] = None
    files: Dict[str, str] = {}


class RunJupyterRequest(BaseModel):
    cells: List[str] = Field(
        ...,
        examples=[[
            'a = 123', 'a', 'print(a)', 'import sys; sys.stderr.write("stderr message")',
            'raise RuntimeError("error message")'
        ]],
        description='list of code blocks to run in jupyter notebook')
    cell_timeout: float = Field(0, description='max run time for each of the cells')
    total_timeout: float = Field(45, description='max run time for all the cells')
    memory_limit_MB: int = Field(-1, description='maximum memory allowed in megabytes')
    kernel: Literal['python3'] = 'python3'
    files: Dict[str, str] = Field({}, description='a dict from file path to base64 encoded file content')
    fetch_files: List[str] = Field([], description='a list of file paths to fetch after code execution')


class CellRunResult(BaseModel):
    stdout: str
    stderr: str
    display: List[Dict[str, Any]]
    error: List[Dict[str, Any]]


class RunJupyterResult(BaseModel):
    status: CommandRunStatus
    driver: CommandRunResult
    cells: List[CellRunResult] = []
    files: Dict[str, str] = {}


Language = Literal['python', 'cpp', 'nodejs', 'go', 'go_test', 'java', 'php', 'csharp', 'bash', 'typescript', 'sql',
                   'rust', 'cuda', 'lua', 'R', 'perl', 'D_ut', 'ruby', 'scala', 'julia', 'pytest', 'junit',
                   'kotlin_script', 'jest', 'verilog', 'python_gpu', 'lean', 'swift', 'racket']
compile_languages: List[Language] = ['cpp', 'go', 'java']
cpu_languages: List[Language] = [
    'python', 'cpp', 'nodejs', 'go', 'go_test', 'java', 'php', 'csharp', 'bash', 'typescript', 'sql', 'rust', 'lua',
    'R', 'perl', 'D_ut', 'ruby', 'scala', 'julia', 'pytest', 'junit', 'kotlin_script', 'jest', 'verilog', 'lean',
    'swift', 'racket'
]
gpu_languages: List[Language] = ['cuda', 'python_gpu']
