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


async def test_humaneval_python_get():
    request = GetPromptsRequest(dataset='humaneval_python', config=TestConfig())
    response = client.post('/get_prompts', json=request.model_dump())
    assert response.status_code == 200
    results = [Prompt(**sample) for sample in response.json()]
    print(results)


async def test_humaneval_python_get_id():
    request = GetPromptByIdRequest(dataset='humaneval_python', id=4, config=TestConfig())
    response = client.post('/get_prompt_by_id', json=request.model_dump())
    assert response.status_code == 200
    result = Prompt(**response.json())
    print(result)


async def test_humaneval_python_list_ids():
    request = GetPromptsRequest(dataset='humaneval_python', config=TestConfig())
    response = client.post('/list_ids', json=request.model_dump())
    assert response.status_code == 200
    print(response.json())


async def test_humaneval_python_submit_passed():
    request = SubmitRequest(dataset='humaneval_python',
                            id=4,
                            config=TestConfig(language='python'),
                            completion='''
    mean = sum(numbers) / len(numbers)
    return sum(abs(x - mean) for x in numbers) / len(numbers)
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


async def test_shadow_humaneval_python_get():
    request = GetPromptsRequest(dataset='shadow_humaneval_python', config=TestConfig())
    response = client.post('/get_prompts', json=request.model_dump())
    assert response.status_code == 200
    results = [Prompt(**sample) for sample in response.json()]
    print(results)


async def test_shadow_humaneval_python_get_id():
    request = GetPromptByIdRequest(dataset='shadow_humaneval_python', id=0, config=TestConfig())
    response = client.post('/get_prompt_by_id', json=request.model_dump())
    assert response.status_code == 200
    result = Prompt(**response.json())
    print(result)


async def test_shadow_humaneval_python_list_ids():
    request = GetPromptsRequest(dataset='shadow_humaneval_python', config=TestConfig())
    response = client.post('/list_ids', json=request.model_dump())
    assert response.status_code == 200
    print(response.json())


async def test_shadow_humaneval_python_submit_passed():
    request = SubmitRequest(
        dataset='shadow_humaneval_python',
        id=0,
        config=TestConfig(),
        completion=
        "\n    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance > threshold:\n                    return True\n\n    return False\n"
    )
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


async def test_humaneval_python_submit_freeform_passed():
    request = SubmitRequest(dataset='humaneval_python',
                            id=0,
                            config=TestConfig(language='python', extra={'is_freeform': True}),
                            completion='''
好的，我将按照你的要求补全代码。

这段 Python 代码定义了一个函数`has_close_elements`，用于检查给定列表中的数字是否存在两个数字之间的距离小于等于给定阈值的情况。

以下是补全后的代码：

```python
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if abs(numbers[i] - numbers[j]) <= threshold:
                return True
    return False
```

在上述代码中，我们使用两个嵌套的循环来遍历列表中的每个数字。对于每个数字，我们检查它后面的数字是否存在距离小于等于阈值的情况。如果存在这样的数字，我们就返回`True`，表示存在两个数字之间的距离小于等于阈值的情况。如果遍历完整个列表都没有找到这样的数字，我们就返回`False`，表示不存在这样的情况。
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


async def test_humaneval_python_submit_freeform_failed():
    request = SubmitRequest(dataset='humaneval_python',
                            id=0,
                            config=TestConfig(language='python'),
                            completion='''
好的，我将按照你的要求补全代码。

这段 Python 代码定义了一个函数`has_close_elements`，用于检查给定列表中的数字是否存在两个数字之间的距离小于等于给定阈值的情况。

以下是补全后的代码：

```python
from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if abs(numbers[i] - numbers[j]) <= threshold:
                return True
    return False
```

在上述代码中，我们使用两个嵌套的循环来遍历列表中的每个数字。对于每个数字，我们检查它后面的数字是否存在距离小于等于阈值的情况。如果存在这样的数字，我们就返回`True`，表示存在两个数字之间的距离小于等于阈值的情况。如果遍历完整个列表都没有找到这样的数字，我们就返回`False`，表示不存在这样的情况。
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False


async def test_humaneval_python_submit_failed():
    request = SubmitRequest(dataset='humaneval_python',
                            id=4,
                            config=TestConfig(language='python'),
                            completion='''
    mean = max(numbers) / len(numbers)
    return sum(abs(x - mean) for x in numbers) / len(numbers)
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False
