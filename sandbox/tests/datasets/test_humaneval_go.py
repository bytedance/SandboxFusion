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


async def test_humaneval_go_get():
    request = GetPromptsRequest(dataset='humaneval_go', config=TestConfig())
    response = client.post('/get_prompts', json=request.model_dump())
    assert response.status_code == 200
    results = [Prompt(**sample) for sample in response.json()]
    print(results)


async def test_humaneval_go_get_id():
    request = GetPromptByIdRequest(dataset='humaneval_go', id=4, config=TestConfig())
    response = client.post('/get_prompt_by_id', json=request.model_dump())
    assert response.status_code == 200
    result = Prompt(**response.json())
    print(result)


async def test_humaneval_go_list_ids():
    request = GetPromptsRequest(dataset='humaneval_go', config=TestConfig())
    response = client.post('/list_ids', json=request.model_dump())
    assert response.status_code == 200
    print(response.json())


async def test_humaneval_go_submit_passed():
    request = SubmitRequest(dataset='humaneval_go',
                            id=4,
                            config=TestConfig(language='go'),
                            completion='''
    n := len(numbers)
    if n == 0 {
        // Return 0 if the input slice is empty
        return 0.0
    }

    // Step 1: Calculate the mean of the numbers
    var sum float64
    for _, number := range numbers {
        sum += number
    }
    mean := sum / float64(n)

    // Step 2: Calculate the absolute differences from the mean
    var totalDeviation float64
    for _, number := range numbers {
        deviation := number - mean
        if deviation < 0 {
            deviation = -deviation // Make it positive
        }
        totalDeviation += deviation
    }

    // Step 3: Calculate the average of these absolute differences
    mad := totalDeviation / float64(n)

    return mad
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


async def test_humaneval_go_submit_failed():
    request = SubmitRequest(dataset='humaneval_go',
                            id=4,
                            config=TestConfig(language='go'),
                            completion='''
    n := len(numbers)
    if n == 0 {
        // Return 0 if the input slice is empty
        return 0.0
    }

    // Step 1: Calculate the mean of the numbers
    var sum float64
    for _, number := range numbers {
        sum += number
    }
    mean := sum / float64(n)

    // Step 2: Calculate the absolute differences from the mean
    var totalDeviation float64
    for _, number := range numbers {
        deviation := number - mean
        if deviation < 0 {
            deviation = -deviation // Make it positive
        }
        totalDeviation -= deviation
    }

    // Step 3: Calculate the average of these absolute differences
    mad := totalDeviation / float64(n)

    return mad
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False


async def test_humaneval_go_freeform_submit_failed():
    request = SubmitRequest(dataset='humaneval_go',
                            id=4,
                            config=TestConfig(extra={'is_freeform': True}),
                            completion='''
    n := len(numbers)
    if n == 0 {
        // Return 0 if the input slice is empty
        return 0.0
    }

    // Step 1: Calculate the mean of the numbers
    var sum float64
    for _, number := range numbers {
        sum += number
    }
    mean := sum / float64(n)

    // Step 2: Calculate the absolute differences from the mean
    var totalDeviation float64
    for _, number := range numbers {
        deviation := number - mean
        if deviation < 0 {
            deviation = -deviation // Make it positive
        }
        totalDeviation += deviation
    }

    // Step 3: Calculate the average of these absolute differences
    mad := totalDeviation / float64(n)

    return mad
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False


async def test_humaneval_go_freeform_submit_passed():
    request = SubmitRequest(dataset='humaneval_go',
                            id=4,
                            config=TestConfig(extra={'is_freeform': True}),
                            completion='''
```go
package mean_absolute_deviation_test

import (
    "testing"
    "fmt"
)

// For a given list of input numbers, calculate Mean Absolute Deviation
// around the mean of this dataset.
// Mean Absolute Deviation is the average absolute difference between each
// element and a centerpoint (mean in this case):
// MAD = average | x - x_mean |
// >>> mean_absolute_deviation([]float64{1.0, 2.0, 3.0, 4.0})
// 1.0
func mean_absolute_deviation(numbers []float64) float64 {
    n := len(numbers)
    if n == 0 {
        // Return 0 if the input slice is empty
        return 0.0
    }

    // Step 1: Calculate the mean of the numbers
    var sum float64
    for _, number := range numbers {
        sum += number
    }
    mean := sum / float64(n)

    // Step 2: Calculate the absolute differences from the mean
    var totalDeviation float64
    for _, number := range numbers {
        deviation := number - mean
        if deviation < 0 {
            deviation = -deviation // Make it positive
        }
        totalDeviation += deviation
    }

    // Step 3: Calculate the average of these absolute differences
    mad := totalDeviation / float64(n)

    return mad
}
```
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True
