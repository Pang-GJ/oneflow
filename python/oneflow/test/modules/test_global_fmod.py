"""
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
import oneflow as flow
import oneflow.unittest

from oneflow.test_utils.automated_test_util import *

import torch as torch_original
from packaging import version

# other.grad in torch.fmod(input, other) was not implemented before pytorch 1.11.0
grad_implemented = version.parse(torch_original.__version__) >= version.parse("1.11.0")


@autotest(n=1, auto_backward=grad_implemented, check_graph=False)
def do_test_fmod_impl(test_case, ndim, placement, sbp):
    dims = [random(1, 4) * 8 for i in range(ndim)]
    x = random_tensor(ndim, *dims)
    x = x.to_global(placement=placement, sbp=sbp)
    y = random_tensor(ndim, *dims)
    y = y.to_global(placement=placement, sbp=sbp)

    z = torch.fmod(x, y)
    return z


class TestFmodGlobal(flow.unittest.TestCase):
    @globaltest
    def test_fmod(test_case):
        # random ndim in range [1,5]
        ndim = random(1, 5).to(int).value()
        for placement in all_placement():
            for sbp in all_sbp(placement, max_dim=ndim):
                do_test_fmod_impl(test_case, ndim, placement, sbp)


if __name__ == "__main__":
    unittest.main()
