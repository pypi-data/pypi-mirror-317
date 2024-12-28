# (c) 2024 Martin Wendt; see https://github.com/mar10/benchman
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
""" """

from benchman import BenchmarkManager, util


class TestBenchmarkManager:
    # @pytest.mark.xfail(reason="just testing")
    def test_bench_init(self, capsys):
        bm = BenchmarkManager.singleton()

        # bm.run_timings(
        #     "sort",
        #     variant="builtin",
        #     repeat=1,  # faster
        #     iterations=10,  # faster
        #     stmt="""\
        #         _ = arr.sort()
        #     """,
        #     setup="arr = [3,2,1]",
        #     sample_size=3,
        #     # globals={"data": data, "fix": fixtures},
        # )

        assert bm

    def test_filter(self):
        assert util.split_tokens("a,b,c") == ["a", "b", "c"]

    def test_smart_sort_keys(self):
        assert sorted(["a", "c", "b"], key=util.smart_sort_key) == ["a", "b", "c"]
        assert sorted(
            ["Py3.10", "Py3.1", "Py3.9.13", "PyPy 2.3"], key=util.smart_sort_key
        ) == [
            "Py3.1",
            "Py3.9.13",
            "Py3.10",
            "PyPy 2.3",
        ]
        assert sorted(["a 10", "a 9,000.1", "a 1.9"], key=util.smart_sort_key) == [
            "a 1.9",
            "a 10",
            "a 9,000.1",
        ]
        assert sorted(
            [
                "sort(quick_sort, n=1,000)",
                "sort(quick_sort, n=100)",
                "sort(quick_sort, n=10)",
            ],
            key=util.smart_sort_key,
        ) == [
            "sort(quick_sort, n=10)",
            "sort(quick_sort, n=100)",
            "sort(quick_sort, n=1,000)",
        ]
