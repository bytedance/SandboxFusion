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

from sandbox.runners import CommandRunStatus
from sandbox.server.sandbox_api import RunCodeRequest, RunCodeResponse, RunStatus
from sandbox.server.server import app

client = TestClient(app)


@pytest.mark.minor
def test_scala_print():
    request = RunCodeRequest(language='scala',
                             code='''
object HelloWorld {
    def main(args: Array[String]): Unit = {
        println("Hello, World!")
    }
}
    ''',
                             compile_timeout=20,
                             run_timeout=5)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    print(result)
    assert result.status == RunStatus.Success
    assert "Hello, World!" in result.run_result.stdout.strip()


@pytest.mark.minor
def test_scala_timeout():
    request = RunCodeRequest(language='scala',
                             code='''
object HelloWorld {
    def main(args: Array[String]): Unit = {
        Thread.sleep(5 * 1000)
        println("Hello, World!")
    }
}
    ''',
                             compile_timeout=20,
                             run_timeout=5)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    assert result.status == RunStatus.Failed
    assert result.run_result.status == CommandRunStatus.TimeLimitExceeded


@pytest.mark.minor
def test_scala_assertion_success():
    request = RunCodeRequest(language='scala',
                             code='''
    object HelloWorld {
        def main(args: Array[String]) = {
            assert((0l) == (0l));
        }
    }
        ''',
                             compile_timeout=20)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    assert result.status == RunStatus.Success
    assert result.run_result.status == CommandRunStatus.Finished

    request = RunCodeRequest(language='scala',
                             code='''
    object Main extends App {
        def foo() = {
            assert((0l) == (0l));
        }

        foo()
    }
        ''',
                             compile_timeout=20)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    assert result.status == RunStatus.Success
    assert result.run_result.status == CommandRunStatus.Finished


@pytest.mark.minor
def test_scala_assertion_error():
    request = RunCodeRequest(language='scala',
                             code='''
object HelloWorld {
    def main(args: Array[String]) = {
        assert((1l) == (0l));
    }
}
    ''',
                             compile_timeout=20)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    assert result.status == RunStatus.Failed
    assert result.run_result.status == CommandRunStatus.Finished
    assert "assertion failed" in result.run_result.stderr

    request = RunCodeRequest(language='scala',
                             code='''
    object Main extends App {
        def foo() = {
            assert((1l) == (0l));
        }

        foo()
    }
        ''',
                             compile_timeout=20)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    assert result.status == RunStatus.Failed
    assert result.run_result.status == CommandRunStatus.Finished
