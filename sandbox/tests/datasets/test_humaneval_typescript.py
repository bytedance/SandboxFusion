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


async def test_humaneval_typescript_get():
    request = GetPromptsRequest(dataset='humaneval_typescript', config=TestConfig())
    response = client.post('/get_prompts', json=request.model_dump())
    assert response.status_code == 200
    results = [Prompt(**sample) for sample in response.json()]
    print(results)


async def test_humaneval_typescript_get_id():
    request = GetPromptByIdRequest(dataset='humaneval_typescript', id=4, config=TestConfig())
    response = client.post('/get_prompt_by_id', json=request.model_dump())
    assert response.status_code == 200
    result = Prompt(**response.json())
    print(result)


async def test_humaneval_typescript_list_ids():
    request = GetPromptsRequest(dataset='humaneval_typescript', config=TestConfig())
    response = client.post('/list_ids', json=request.model_dump())
    assert response.status_code == 200
    print(response.json())


async def test_humaneval_typescript_submit_passed():
    request = SubmitRequest(dataset='humaneval_typescript',
                            id=4,
                            config=TestConfig(language='typescript'),
                            completion='''
    // Step 1: Calculate the mean of the numbers
    const mean = numbers.reduce((acc, val) => acc + val, 0) / numbers.length;

    // Step 2: Calculate the absolute differences from the mean
    const absoluteDifferences = numbers.map(value => Math.abs(value - mean));

    // Step 3: Calculate the average of these absolute differences
    const mad = absoluteDifferences.reduce((acc, val) => acc + val, 0) / numbers.length;

    return mad;
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


async def test_humaneval_typescript_submit_failed():
    request = SubmitRequest(dataset='humaneval_typescript',
                            id=4,
                            config=TestConfig(language='typescript'),
                            completion='''
    // Step 1: Calculate the mean of the numbers
    const mean = numbers.reduce((acc, val) => acc + val, 0) / numbers.length;

    // Step 2: Calculate the absolute differences from the mean
    const absoluteDifferences = numbers.map(value => Math.abs(value + mean));

    // Step 3: Calculate the average of these absolute differences
    const mad = absoluteDifferences.reduce((acc, val) => acc + val, 0) / numbers.length;

    return mad;
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False


async def test_humaneval_typescript_freeform_submit_passed():
    request = SubmitRequest(dataset='humaneval_typescript',
                            id=0,
                            config=TestConfig(language='typescript', extra={'is_freeform': True}),
                            completion='''
好的，我将按照你的要求补全代码。

这段代码的功能是检查给定的数字数组中是否存在两个数字之间的距离小于等于给定阈值的情况。

以下是补全后的代码：

```typescript
//Check if in given array of numbers, are any two numbers closer to each other than
// given threshold.
// >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
// false
// >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
// true
function has_close_elements(numbers: number[], threshold: number): boolean {
    for (let i = 0; i < numbers.length; i++) {
        for (let j = i + 1; j < numbers.length; j++) {
            if (Math.abs(numbers[i] - numbers[j]) <= threshold) {
                return true;
            }
        }
    }
    return false;
}
```

在上述代码中，我们使用两个嵌套的循环来遍历数组中的每个数字。对于每个数字，我们检查它后面的数字是否与它之间的距离小于等于阈值。如果找到这样的数字，我们立即返回 `true`。如果在整个数组中都没有找到这样的数字，我们返回 `false`。
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


async def test_humaneval_typescript_freeform_submit_failed():
    request = SubmitRequest(dataset='humaneval_typescript',
                            id=4,
                            config=TestConfig(language='typescript', extra={'is_freeform': True}),
                            completion='''
    // Step 1: Calculate the mean of the numbers
    const mean = numbers.reduce((acc, val) => acc + val, 0) / numbers.length;

    // Step 2: Calculate the absolute differences from the mean
    const absoluteDifferences = numbers.map(value => Math.abs(value + mean));

    // Step 3: Calculate the average of these absolute differences
    const mad = absoluteDifferences.reduce((acc, val) => acc + val, 0) / numbers.length;

    return mad;
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False
