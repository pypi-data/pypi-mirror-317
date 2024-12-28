# (c) 2024 Martin Wendt; see https://github.com/mar10/benchman
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
""" """
# ruff: noqa: T201, T203 `print` found
# ruff: noqa: E501 Line too long

import sys

import pytest
from benchman import BenchmarkManager

from . import fixtures  # noqa: F401

benchmark = pytest.mark.skipif(
    "--benchmarks" not in sys.argv,
    reason="`--benchmarks` not set",
)


@benchmark
class TestBenchmarks:
    # @pytest.mark.xfail(reason="just testing")

    def _test_sort_suite(self, *, bm: BenchmarkManager, data: list):
        """ """
        bmr = bm.make_runner(name="sort", sample_size=len(data))
        bmr.run(
            variant="quick_sort",
            stmt="""\
                _ = fix.quick_sort(arr)
            """,
            setup="arr = data.copy()",
            globals={"data": data, "fix": fixtures},
        )
        bmr.run(
            variant="bubble_sort",
            stmt="""\
                _ = fix.bubble_sort(arr)
            """,
            setup="arr = data.copy()",
            globals={"data": data, "fix": fixtures},
        )
        bmr.run(
            variant="insertion_sort",
            stmt="""\
                _ = fix.insertion_sort(arr)
            """,
            setup="arr = data.copy()",
            globals={"data": data, "fix": fixtures},
        )
        bmr.run(
            variant="builtin",
            stmt="""\
                _ = fix.native_sort(arr)
            """,
            setup="arr = data.copy()",
            globals={"data": data, "fix": fixtures},
        )
        return bmr

    def test_bench_sort(self, capsys, benchman):
        self._test_sort_suite(bm=benchman, data=fixtures.SMALL_RANDOM_ARRAY)
        self._test_sort_suite(bm=benchman, data=fixtures.MEDIUM_RANDOM_ARRAY)
        self._test_sort_suite(bm=benchman, data=fixtures.LARGE_RANDOM_ARRAY)

        with capsys.disabled():
            print(f"\n{benchman}")
            benchman.print_results()
