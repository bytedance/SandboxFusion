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

from fastapi.testclient import TestClient

from sandbox.datasets.types import EvalResult, Prompt, TestConfig
from sandbox.server.online_judge_api import GetPromptByIdRequest, GetPromptsRequest, SubmitRequest
from sandbox.server.server import app

client = TestClient(app)


async def test_mbpp_get():
    request = GetPromptsRequest(dataset='mbpp', config=TestConfig())
    response = client.post('/get_prompts', json=request.model_dump())
    assert response.status_code == 200
    results = [Prompt(**sample) for sample in response.json()]
    print(results)


async def test_mbpp_get_id():
    request = GetPromptByIdRequest(dataset='mbpp', id=14, config=TestConfig())
    response = client.post('/get_prompt_by_id', json=request.model_dump())
    assert response.status_code == 200
    result = Prompt(**response.json())
    print(result)


async def test_mbpp_list_ids():
    request = GetPromptsRequest(dataset='mbpp', config=TestConfig())
    response = client.post('/list_ids', json=request.model_dump())
    assert response.status_code == 200
    print(response.json())


async def test_mbpp_submit_passed():
    request = SubmitRequest(dataset='mbpp',
                            id=14,
                            config=TestConfig(language='python'),
                            completion='''
```python
def find_Volume(l,b,h) : 
    return ((l * b * h) / 2)
```
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


async def test_mbpp_submit_failed():
    request = SubmitRequest(dataset='mbpp',
                            id=14,
                            config=TestConfig(language='python'),
                            completion='''
    mean = max(numbers) / len(numbers)
    return sum(abs(x - mean) for x in numbers) / len(numbers)
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False
