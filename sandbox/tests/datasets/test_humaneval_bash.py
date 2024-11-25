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


async def test_humaneval_bash_get():
    request = GetPromptsRequest(dataset='humaneval_bash', config=TestConfig())
    response = client.post('/get_prompts', json=request.model_dump())
    assert response.status_code == 200
    results = [Prompt(**sample) for sample in response.json()]
    print(results)


async def test_humaneval_bash_get_id():
    request = GetPromptByIdRequest(dataset='humaneval_bash', id=4, config=TestConfig())
    response = client.post('/get_prompt_by_id', json=request.model_dump())
    assert response.status_code == 200
    result = Prompt(**response.json())
    print(result)


async def test_humaneval_bash_list_ids():
    request = GetPromptsRequest(dataset='humaneval_bash', config=TestConfig())
    response = client.post('/list_ids', json=request.model_dump())
    assert response.status_code == 200
    print(response.json())


async def test_humaneval_bash_submit_passed():
    request = SubmitRequest(dataset='humaneval_bash',
                            id=12,
                            config=TestConfig(language='bash'),
                            completion='''
    # Check if the input is empty
    if [ -z "$1" ]; then
        echo "None"
        return
    fi

    # Initialize variables to keep track of the longest string and its length
    local longest=""
    local max_length=0

    # Iterate over each word in the input (split by spaces)
    for word in $1; do
        # Get the length of the current word
        local length=${#word}
        
        # Update the longest word if this word is longer
        if [ $length -gt $max_length ]; then
            longest=$word
            max_length=$length
        fi
    done

    # Output the longest word
    echo "$longest"
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == True


async def test_humaneval_bash_submit_failed():
    request = SubmitRequest(dataset='humaneval_bash',
                            id=12,
                            config=TestConfig(language='bash'),
                            completion='''
    # Check if the input is empty
    if [ -z "$1" ]; then
        echo "None"
        return
    fi

    # Initialize variables to keep track of the longest string and its length
    local longest=""
    local max_length=0

    # Iterate over each word in the input (split by spaces)
    for word in $1; do
        # Get the length of the current word
        local length=${#word}
        
        # Update the longest word if this word is longer
        if [ $length -gt $max_length ]; then
            longest=$word
            max_length=$length
        fi
    done

    # Output the longest word
    echo "123$longest"
}
''')
    response = client.post('/submit', json=request.model_dump())
    assert response.status_code == 200
    result = EvalResult(**response.json())
    assert result.accepted == False
