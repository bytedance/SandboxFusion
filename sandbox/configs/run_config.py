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

import os
from typing import Dict, List, Literal, Optional, Union

import structlog
import yaml
from pydantic import BaseModel

logger = structlog.stdlib.get_logger()


class RunConfig(BaseModel):

    class DatasetConfig(BaseModel):

        class DataBase(BaseModel):

            class Backend(BaseModel):
                type: Literal['mysql', 'none']
                user: Optional[str] = None
                password: Optional[str] = None
                psm: Optional[str] = None
                host: Optional[str] = None
                port: Optional[str] = None

            class Cache(BaseModel):

                class CacheSourceLocal(BaseModel):
                    type: Literal['local']
                    path: str

                class CacheSourceMysql(BaseModel):

                    class MysqlTable(BaseModel):
                        name: str
                        columns: List[str]

                    type: Literal['mysql']
                    tables: List[MysqlTable]

                # memory / local db location
                path: str
                sources: List[Union[CacheSourceLocal, CacheSourceMysql]]

            backend: Backend
            cache: Optional[Cache] = None

        class RegistryItem(BaseModel):
            module_path: str
            class_name: str
            dataset_tables: Dict[str, str] = {}

        database: DataBase
        max_runner_concurrency: int = 0
        cpu_runner_url: Optional[str] = None
        gpu_runner_url: Optional[str] = None
        default_dataset_table: str = 'code_eval_${dataset_id}'
        registry: List[RegistryItem] = []

    class SandboxConfig(BaseModel):
        '''
        none: no isolation, cleanup_process and restore_bash are best effort for correctness
        lite: handcrafted overlayfs + chroot + cgroups isolation, fast (< 100 ms overhead)
        foil: each command under `foil run --strict` (https://github.com/ai-agentic-tools/Foil), no root needed
        '''
        isolation: Literal['none', 'lite', 'foil']
        set_uid: Optional[int] = None
        cleanup_process: bool
        restore_bash: bool
        # overselling is key to reduce cost
        max_concurrency: int

    class Common(BaseModel):
        logging_color: bool

    sandbox: SandboxConfig
    dataset: DatasetConfig
    common: Common

    def __init__(self):
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), f'{os.getenv("SANDBOX_CONFIG", "local")}.yaml'))
        # logger.info(f'loading config from {config_path}')
        with open(config_path) as f:
            data = yaml.safe_load(f)
        super().__init__(**data)

    # moved sigleton logic here until type inference is fixed
    _instance: Optional['RunConfig'] = None

    @classmethod
    def get_instance_sync(cls, *args, **kwargs) -> 'RunConfig':
        if not cls.__private_attributes__['_instance'].default:
            self = cls(*args, **kwargs)
            assert not hasattr(
                self, 'async_init'), f'class {cls.__name__} has async_init function, init it with get_instance_async.'
            cls.__private_attributes__['_instance'].default = self
            logger.debug('singleton class initialized', name=cls.__name__)
        return cls.__private_attributes__['_instance'].default
