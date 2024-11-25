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

import inspect

from sandbox.datasets.humaneval_deprecated import HumanEvalDeprecatedDataset
from sandbox.datasets.types import SubmitRequest
from sandbox.utils.extraction import extract_code_from_freeform_completion


def get_categories(results):
    import re
    from collections import defaultdict
    categories_counts = defaultdict(list)
    for r in results:
        task_id = r.id
        cate_pattern = r'EvoEval_(.*)_EvoEval'
        cate = re.findall(cate_pattern, task_id)[0]
        categories_counts[cate].append(r)

    return categories_counts


class EvoEvalDataset(HumanEvalDeprecatedDataset):

    @classmethod
    def _gen_pretrain_code(cls, request: SubmitRequest, row) -> str:
        completion = request.completion
        prompt = cls._generate_single_prompt(row, request.dataset, request.config).prompt
        code, _ = extract_code_from_freeform_completion(f'{prompt}\n{completion}',
                                                        cls.extract_lang_map[request.dataset],
                                                        first_block_only=True)
        full_code = f"{code}\n{row['test']}"
        return completion, full_code

    @classmethod
    def get_metrics_function(cls) -> str:
        source = f'''
{inspect.getsource(get_categories)}

def pass_at_k_v2(samples, n: int, k: int) -> float:
    import numpy

    def codex_estimator(n: int, c: int, k: int) -> float:
        """
        Calculates 1 - comb(n - c, k) / comb(n, k).
        """
        if n - c < k:
            return 1.0
        return 1.0 - numpy.prod(1.0 - k / numpy.arange(n - c + 1, n + 1))

    from collections import defaultdict
    """ Compute Pass@k metric.
        Args:
            samples: list of (task_name/id, passed) pair
            n: total sample times
        Returns:
            final average Pass@k score
    """
    correct_dict = defaultdict(int)
    for name, passed in samples:
        if passed:
            correct_dict[name] += 1
        else:
            correct_dict[name] += 0

    final_scores = []
    for _, c in correct_dict.items():
        score = codex_estimator(n, c, k)
        final_scores.append(score)
    if final_scores:
        final_score = sum(final_scores) / len(final_scores)
    else:
        final_score = 0.0  # empty case

    return final_score

def get_metrics(results):
    categories = get_categories(results)
    performance = {{}}
    for cat, samples in categories.items():
        for k in k_targets:
            if repeats < k:
                continue
            pak = pass_at_k_v2([(s.id, s.accepted) for s in samples], repeats, k)
            performance[f'{{cat}}/Pass@k={{k}}'] = pak
    return performance
'''
        return source
