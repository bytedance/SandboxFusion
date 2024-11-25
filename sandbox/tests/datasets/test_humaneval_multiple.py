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
from sandbox.utils.common import load_jsonl
import os

client = TestClient(app)

samples_directory = os.path.join(os.path.dirname(__file__), 'samples', 'Multi-PLE')


async def test_humaneval_multiple_get():
    for path in os.listdir(samples_directory):
        samples_path = os.path.join(samples_directory, path)
        lang = path.split('.')[0]

        samples = load_jsonl(samples_path)
        request = GetPromptsRequest(dataset=lang,
                                    config=TestConfig(dataset_type='HumanEvalDataset', provided_data=samples))
        response = client.post('/get_prompts', json=request.model_dump())
        assert response.status_code == 200
        results = [Prompt(**sample) for sample in response.json()]
        print(results[0].labels)

        request = GetPromptsRequest(dataset=lang,
                                    config=TestConfig(dataset_type='HumanEvalDataset',
                                                      provided_data=samples,
                                                      extra={'is_freeform': True}))
        response = client.post('/get_prompts', json=request.model_dump())
        assert response.status_code == 200
        results = [Prompt(**sample) for sample in response.json()]
        print(results[0].prompt)


async def test_humaneval_multiple_get_single():
    for path in os.listdir(samples_directory):
        samples_path = os.path.join(samples_directory, path)
        lang = path.split('.')[0]

        sample = load_jsonl(samples_path)[0]
        request = GetPromptByIdRequest(dataset=lang,
                                       config=TestConfig(dataset_type='HumanEvalDataset', provided_data=sample),
                                       id=0)
        response = client.post('/get_prompt_by_id', json=request.model_dump())
        assert response.status_code == 200
        result = Prompt(**response.json())
        print(result.prompt)

        request = GetPromptByIdRequest(dataset=lang,
                                       config=TestConfig(dataset_type='HumanEvalDataset',
                                                         provided_data=sample,
                                                         extra={'is_freeform': True}),
                                       id=0)
        response = client.post('/get_prompt_by_id', json=request.model_dump())
        assert response.status_code == 200
        result = Prompt(**response.json())
        print(result.prompt)


async def test_humaneval_multiple_submit_passed():
    for path in os.listdir(samples_directory):
        samples_path = os.path.join(samples_directory, path)
        lang = path.split('.')[0]
        if 'go' in lang:
            sample = load_jsonl(samples_path)[1]
        else:
            sample = load_jsonl(samples_path)[3]
        solution = sample['gpt_solution']
        request = SubmitRequest(dataset=lang,
                                id=0,
                                config=TestConfig(dataset_type='HumanEvalDataset',
                                                  provided_data=sample,
                                                  extra={'is_freeform': True}),
                                completion=solution)
        response = client.post('/submit', json=request.model_dump())
        assert response.status_code == 200
        result = EvalResult(**response.json())
        assert result.accepted == True
