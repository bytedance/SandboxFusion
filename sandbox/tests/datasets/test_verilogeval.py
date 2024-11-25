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

import pytest
from fastapi.testclient import TestClient

from sandbox.datasets.types import EvalResult, Prompt, TestConfig
from sandbox.server.online_judge_api import GetPromptByIdRequest, GetPromptsRequest, SubmitRequest
from sandbox.server.server import app

client = TestClient(app)


@pytest.mark.parametrize("dataset", ['verilogeval_human', 'verilogeval_machine'])
async def test_verilog_get(dataset):
    request = GetPromptsRequest(dataset=dataset, config=TestConfig())
    response = client.post('/get_prompts', json=request.model_dump())
    assert response.status_code == 200
    results = [Prompt(**sample) for sample in response.json()]
    # print(results)


@pytest.mark.parametrize("dataset", ['verilogeval_human', 'verilogeval_machine'])
@pytest.mark.parametrize("is_fewshot", [True, False])
async def test_verilog_get_id(dataset, is_fewshot):
    request = GetPromptByIdRequest(dataset=dataset, id=0, config=TestConfig(is_fewshot=is_fewshot))
    response = client.post('/get_prompt_by_id', json=request.model_dump())
    assert response.status_code == 200
    result = Prompt(**response.json())
    print(result)


@pytest.mark.parametrize("dataset, id", [("verilogeval_human", 0), ("verilogeval_machine", 73)])
@pytest.mark.parametrize("is_fewshot", [True, False])
async def test_verilog_submitWithoutBlock(dataset, id, is_fewshot):
    request = SubmitRequest(dataset=dataset,
                            id=id,
                            config=TestConfig(language='verilog', is_fewshot=is_fewshot),
                            completion='''
    assign out = sel ? b : a;
endmodule
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


@pytest.mark.parametrize("dataset, id", [("verilogeval_human", 0), ("verilogeval_machine", 73)])
@pytest.mark.parametrize("is_fewshot", [True, False])
async def test_verilog_submitWithBlock(dataset, id, is_fewshot):
    request = SubmitRequest(dataset=dataset,
                            id=id,
                            config=TestConfig(language='verilog', is_fewshot=is_fewshot),
                            completion='''
```verilog
    assign out = sel ? b : a;
endmodule
```
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


@pytest.mark.parametrize("dataset, id", [("verilogeval_human", 0), ("verilogeval_machine", 73)])
@pytest.mark.parametrize("is_fewshot", [True, False])
async def test_verilog_submitWithAdditionalText(dataset, id, is_fewshot):
    request = SubmitRequest(dataset=dataset,
                            id=id,
                            config=TestConfig(language='verilog', is_fewshot=is_fewshot),
                            completion='''
Following is the full code.
```verilog
module top_module (
    input [99:0] a,
    input [99:0] b,
    input sel,
    output [99:0] out);
assign out = sel ? b : a;
endmodule
```
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


@pytest.mark.parametrize("dataset, id", [("verilogeval_human", 0), ("verilogeval_machine", 73)])
@pytest.mark.parametrize("is_fewshot", [True, False])
async def test_verilog_submitWithLanguageAlias(dataset, id, is_fewshot):
    request = SubmitRequest(dataset=dataset,
                            id=id,
                            config=TestConfig(language='verilog', is_fewshot=is_fewshot),
                            completion='''
```Verilog
    assign out = sel ? b : a;
endmodule
```
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


@pytest.mark.parametrize("dataset, id", [("verilogeval_human", 0), ("verilogeval_machine", 73)])
@pytest.mark.parametrize("is_fewshot", [True, False])
async def test_verilog_CompileError(dataset, id, is_fewshot):
    request = SubmitRequest(dataset=dataset,
                            id=id,
                            config=TestConfig(language='verilog', is_fewshot=is_fewshot),
                            completion='''
```Verilog
    assign out = sel ? b : a;
```
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False
