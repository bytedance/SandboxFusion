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


async def test_humaneval_java_get():
    request = GetPromptsRequest(dataset='humaneval_java', config=TestConfig())
    response = client.post('/get_prompts', json=request.model_dump())
    assert response.status_code == 200
    results = [Prompt(**sample) for sample in response.json()]
    print(results)


async def test_humaneval_java_get_id():
    request = GetPromptByIdRequest(dataset='humaneval_java', id=4, config=TestConfig())
    response = client.post('/get_prompt_by_id', json=request.model_dump())
    assert response.status_code == 200
    result = Prompt(**response.json())
    print(result)


async def test_humaneval_java_list_ids():
    request = GetPromptsRequest(dataset='humaneval_java', config=TestConfig())
    response = client.post('/list_ids', json=request.model_dump())
    assert response.status_code == 200
    print(response.json())


async def test_humaneval_java_submit_passed():
    request = SubmitRequest(dataset='humaneval_java',
                            id=4,
                            config=TestConfig(language='java'),
                            completion='''
        if (numbers == null || numbers.isEmpty()) {
            throw new IllegalArgumentException("The input list cannot be null or empty");
        }

        // Calculate the mean of the numbers
        float sum = 0;
        for (float num : numbers) {
            sum += num;
        }
        float mean = sum / numbers.size();

        // Calculate the Mean Absolute Deviation (MAD)
        float totalDeviation = 0;
        for (float num : numbers) {
            totalDeviation += Math.abs(num - mean);
        }
        float mad = totalDeviation / numbers.size();

        return mad;
    }

    public static void main(String[] args) {
        ArrayList<Float> data = new ArrayList<>(Arrays.asList(1.0f, 2.0f, 3.0f, 4.0f));
        System.out.println("Mean Absolute Deviation: " + meanAbsoluteDeviation(data));
    }
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


async def test_humaneval_java_submit_failed():
    request = SubmitRequest(dataset='humaneval_java',
                            id=4,
                            config=TestConfig(language='java'),
                            completion='''
        if (numbers == null || numbers.isEmpty()) {
            throw new IllegalArgumentException("The input list cannot be null or empty");
        }

        // Calculate the mean of the numbers
        float sum = 0;
        for (float num : numbers) {
            sum += num;
        }
        float mean = sum / numbers.size();

        // Calculate the Mean Absolute Deviation (MAD)
        float totalDeviation = 10;
        for (float num : numbers) {
            totalDeviation += Math.abs(num - mean);
        }
        float mad = totalDeviation / numbers.size();

        return mad;
    }

    public static void main(String[] args) {
        ArrayList<Float> data = new ArrayList<>(Arrays.asList(1.0f, 2.0f, 3.0f, 4.0f));
        System.out.println("Mean Absolute Deviation: " + meanAbsoluteDeviation(data));
    }
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False


async def test_humaneval_java_freeform_submit_passed():
    request = SubmitRequest(dataset='humaneval_java',
                            id=4,
                            config=TestConfig(extra={'is_freeform': True}),
                            completion='''
```java
import java.util.*;
import java.lang.reflect.*;
import org.javatuples.*;
import java.security.*;
import java.math.*;
import java.io.*;
import java.util.stream.*;
class Problem {
    // For a given array list of input numbers, calculate Mean Absolute Deviation
    // around the mean of this dataset.
    // Mean Absolute Deviation is the average absolute difference between each
    // element and a centerpoint (mean in this case):
    // MAD = average | x - x_mean |
    // >>> meanAbsoluteDeviation((new ArrayList<Float>(Arrays.asList((float)1.0f, (float)2.0f, (float)3.0f, (float)4.0f))))
    // (1.0f)
    public static float meanAbsoluteDeviation(ArrayList<Float> numbers) {
        if (numbers == null || numbers.isEmpty()) {
            throw new IllegalArgumentException("The input list cannot be null or empty");
        }

        // Calculate the mean of the numbers
        float sum = 0;
        for (float num : numbers) {
            sum += num;
        }
        float mean = sum / numbers.size();

        // Calculate the Mean Absolute Deviation (MAD)
        float totalDeviation = 0;
        for (float num : numbers) {
            totalDeviation += Math.abs(num - mean);
        }
        float mad = totalDeviation / numbers.size();

        return mad;
    }

    public static void main(String[] args) {
        ArrayList<Float> data = new ArrayList<>(Arrays.asList(1.0f, 2.0f, 3.0f, 4.0f));
        System.out.println("Mean Absolute Deviation: " + meanAbsoluteDeviation(data));
    }
}
```
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


async def test_humaneval_java_freeform_submit_failed():
    request = SubmitRequest(dataset='humaneval_java',
                            id=4,
                            config=TestConfig(extra={'is_freeform': True}),
                            completion='''
        if (numbers == null || numbers.isEmpty()) {
            throw new IllegalArgumentException("The input list cannot be null or empty");
        }

        // Calculate the mean of the numbers
        float sum = 0;
        for (float num : numbers) {
            sum += num;
        }
        float mean = sum / numbers.size();

        // Calculate the Mean Absolute Deviation (MAD)
        float totalDeviation = 10;
        for (float num : numbers) {
            totalDeviation += Math.abs(num - mean);
        }
        float mad = totalDeviation / numbers.size();

        return mad;
    }

    public static void main(String[] args) {
        ArrayList<Float> data = new ArrayList<>(Arrays.asList(1.0f, 2.0f, 3.0f, 4.0f));
        System.out.println("Mean Absolute Deviation: " + meanAbsoluteDeviation(data));
    }
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False
