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
from typing import Dict, Literal, Optional, List, Any, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from pydantic.v1 import BaseModel, Field
else:
    try:
        from pydantic.v1 import BaseModel, Field
    except ImportError:
        from pydantic import BaseModel, Field

# Sandbox related


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
    files: Dict[str, str] = {}
    compile_timeout: float = 10
    run_timeout: float = 10
    stdin: Optional[str] = None
    fetch_files: List[str] = []


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
    kernel: Literal['python3'] = 'python3'
    files: Dict[str, str] = Field(default_factory=dict, description='a dict from file path to base64 encoded file content')
    fetch_files: List[str] = Field(default_factory=list, description='a list of file paths to fetch after code execution')


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


class CommandRunStatus(str, Enum):
    Finished = 'Finished'
    TimeLimitExceeded = 'TimeLimitExceeded'
    # ignore this in logic as this state cause run_code to throw
    Error = 'Error'


class CommandRunResult(BaseModel):
    status: CommandRunStatus
    execution_time: Optional[float] = None
    return_code: Optional[int] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None


class RunStatus(str, Enum):
    # all command finished successfully
    Success = 'Success'
    # one of the process has non-zero return code
    Failed = 'Failed'
    # error on sandbox side, ignore this in logic as this state cause run_code to throw
    SandboxError = 'SandboxError'


class RunCodeRequest(BaseModel):
    compile_timeout: float = Field(10, description='compile timeout for compiled languages')
    run_timeout: float = Field(10, description='code run timeout')
    code: str = Field(..., examples=['print("hello")'], description='the code to run')
    stdin: Optional[str] = Field(None, examples=[''], description='optional string to pass into stdin')
    language: Language = Field(..., examples=['python'], description='the language or execution mode to run the code')
    files: Dict[str, Optional[str]] = Field(default_factory=dict, description='a dict from file path to base64 encoded file content')
    fetch_files: List[str] = Field(default_factory=list, description='a list of file paths to fetch after code execution')


class RunCodeResponse(BaseModel):
    status: RunStatus
    message: str
    compile_result: Optional[CommandRunResult] = None
    run_result: Optional[CommandRunResult] = None
    executor_pod_name: Optional[str] = None
    files: Dict[str, str] = {}


class RunJupyterResponse(BaseModel):
    status: RunStatus
    message: str
    driver: Optional[CommandRunResult] = None
    cells: List[CellRunResult] = []
    executor_pod_name: Optional[str] = None
    files: Dict[str, str] = {}


class SummaryMapping(BaseModel):
    Success: str = RunStatus.Success
    Failed: str = RunStatus.Failed
    CompileFailed: Optional[str] = None
    CompileTimeout: Optional[str] = None
    RunFailed: Optional[str] = None
    RunTimeout: Optional[str] = None


# Datasets related


class Prompt(BaseModel):
    id: Union[int, str]
    prompt: str
    labels: Dict[str, Any] = {}


class TestConfig(BaseModel):
    '''
    custom_extract_logic: a piece of python code that calls `submit_code_blocks(cbs)` to extract custom code
                          cbs: List[CodeBlock], CodeBlock(priority=40, code='xxx', language='xxx')
                          priority: fenced = 30, incomplete fenced = 20, heuristic = 10
    '''
    __test__ = False
    dataset_type: Optional[str] = Field(
        None,
        examples=[None],
        description='the dataset class used to process, only works when the dataset id is not registered.')
    language: Optional[Language] = None
    locale: Optional[str] = None
    is_fewshot: Optional[bool] = None
    compile_timeout: Optional[float] = None
    run_timeout: Optional[float] = None
    custom_extract_logic: Optional[str] = None
    provided_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]] = None
    extra: Dict[str, Any] = {}


class GeneralStdioTest(BaseModel):
    # stdin / stdout for the standard streams, other names for files
    input: Dict[str, str]
    output: Dict[str, str]


class EvalTestCase(BaseModel):
    passed: bool
    exec_info: RunCodeResponse
    test_info: Optional[Dict[str, Any]] = None


class EvalResult(BaseModel):
    id: Union[int, str]
    accepted: bool
    extracted_code: str
    full_code: Optional[str] = None
    test_code: Optional[str] = None
    tests: List[EvalTestCase]
    extracted_type: Optional[Literal['fenced', 'incomplete_fenced', 'heuristic', 'empty']] = None
    extra: Optional[Dict] = None


class GetPromptsRequest(BaseModel):
    dataset: str
    config: TestConfig
    offset: int = 0
    limit: int = 1000000


class GetPromptByIdRequest(BaseModel):
    dataset: str
    config: TestConfig
    id: Union[int, str]


class SubmitRequest(BaseModel):
    dataset: str
    id: Union[int, str]
    completion: str
    config: TestConfig


class GetMetricsRequest(BaseModel):
    dataset: str
    config: TestConfig
    results: List[EvalResult]


class GetMetricsFunctionRequest(BaseModel):
    dataset: str
    config: TestConfig


class GetMetricsFunctionResult(BaseModel):
    function: Optional[str]
