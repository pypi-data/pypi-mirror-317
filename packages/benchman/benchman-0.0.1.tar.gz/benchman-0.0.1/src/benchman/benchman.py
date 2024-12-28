# (c) 2024 Martin Wendt; see https://github.com/mar10/benchman
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
""" """

from __future__ import annotations

import json
import logging
import math
import time
import timeit
import warnings
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from typing_extensions import Self

from benchman.context_info import BaseContextInfo
from benchman.timings import TimingsResult, run_timings
from benchman.util import (
    TTimeUnit,
    byte_number_string,
    format_time,
    get_time_unit,
    json_dump,
    sluggify,
)

logger = logging.getLogger("benchman")


TAG_LATEST = "latest"
TAG_BASE = "base"


# @dataclass_transform()
@dataclass
class IQRValues:
    q1: float
    q3: float
    iqr: float
    lower_bound: float
    upper_bound: float


def get_benchmark_filepath(tag_or_path: Path | str, *, must_exist=False) -> Path:
    """Return the path to the benchmark file for the given tag or path."""

    if isinstance(tag_or_path, Path) or "." in tag_or_path:
        #  Assume this is a path to a file
        path = Path(tag_or_path)
        if not str(path).endswith(".bench.json"):
            raise ValueError(f"Expected file extension '.bench.json': {path}")
    else:
        # Assume this is a tag
        bm = BenchmarkManager.singleton()
        file_name = bm.make_slug(tag=tag_or_path)
        path = bm.folder / f"{file_name}.bench.json"

        # path_list = list(folder.glob(f"*.{tag_or_path}.bench.json"))
        # if not path_list:
        #     raise FileNotFoundError(
        #         f"No benchmark file found for tag '{tag_or_path}' in {folder}"
        #     )
        # ifuv len(path_list) > 1:
        #     msg = (
        #   f"Multiple benchmark files found for tag '{tag_or_path}' in {folder}:\n"
        #         f"  {path_list}"
        #     )
        #     raise ValueError(msg)
        # path = path_list[0]

    if must_exist and not path.is_file():
        raise FileNotFoundError(path)

    return path


class Benchmark:
    """One single micro benchmark run.

    Note: it's tempting to calculate mean and standard deviation from the result
    vector and report these.  However, this is not very useful.
    In a typical case, the lowest value gives a lower bound for how fast your
    machine can run the given code snippet; higher values in the result vector
    are typically not caused by variability in Python's speed, but by other
    processes interfering with your timing accuracy.
    So the min() of the result is probably the only number you should be
    interested in.
    After that, you should look at the entire vector and apply common sense
    rather than statistics.
    """

    def __init__(
        self, benchmark_manager: BenchmarkManager, name: str, *, variant: str = ""
    ):
        assert name, "name must not be empty"

        self.benchmark_manager: BenchmarkManager = benchmark_manager
        #: A name for this benchmark.
        self.name: str = name.strip()
        #: A variant name for this benchmark run (optional, defaults to "").
        self.variant: str = variant.strip()
        #: Python implementatoin and version number
        self.python: str = ""
        # #: Suite tag
        # self.tag: str = ""
        # #: Project name
        # self.project: str = ""
        # #: Project version number
        # self.version: str = ""
        #: Start time of this benchmark run
        self.start_time: float = 0.0
        #: Total time for the whole benchmark loop
        self.elap: float = 0.0
        #: Informational detail, e.g. the number of items processed in one run.
        #: Can be used to evalue the implact of the sample size on the performance.
        self.sample_size: int = 1
        #: Number of iterations in one run (used for 'items per sec.')
        self.iterations: int = 0
        #: List of timings for each run divided by `iterations`, i.e. 'seconds per
        #: iteration'
        self.timings: list[float] = []
        # The interquartile range (IQR) is a measure of statistical dispersion,
        # (cached for performance)
        self._iqr_values: IQRValues | None = None

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.full_name}, {self.elap}s>"

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Benchmark):
            return NotImplemented
        return self.min < other.min

    def to_str(self, *, time_unit: TTimeUnit | None = None) -> str:
        return "{}: {:,d} loop{}, best of {:,}: {} per loop ({} per sec.)".format(
            self.full_name,
            self.iterations,
            "" if self.iterations == 1 else "s",
            self.repeat,
            format_time(self.min, unit=time_unit),
            byte_number_string(self.iterations / self.min),
        )

    @property
    def full_name(self) -> str:
        variant = self.variant
        if self.sample_size > 1:
            if variant:
                variant += ", "
            variant += f"n={self.sample_size:,}"
        return f"{self.name}({variant})" if variant else self.name

    @property
    def version(self) -> str:
        return str(self.benchmark_manager.loaded_context["version"])

    @property
    def tag(self) -> str:
        return str(self.benchmark_manager.loaded_context["tag"])

    @property
    def project(self) -> str:
        return str(self.benchmark_manager.loaded_context["project"])

    @property
    def repeat(self) -> int:
        return len(self.timings)

    @property
    def min(self) -> float:
        return min(self.timings)

    @property
    def max(self) -> float:
        return max(self.timings)

    @property
    def mean(self) -> float:
        """Return the arithmetic average time per iteration, aka 'X̄'."""
        return sum(self.timings) / len(self.timings)

    @property
    def stdev(self) -> float:
        """Return the standard deviation of the time per iteration (aka SD, σ)."""
        n = len(self.timings)

        if n <= 1:
            return 0.0
        mean: float = self.mean
        return math.sqrt(sum((x - mean) ** 2 for x in self.timings) / n)

    @property
    def median(self) -> float:
        """Return the median time per iteration (aka med(x))."""
        timings = sorted(self.timings)
        n = len(timings)
        if n % 2 == 0:
            return (timings[n // 2 - 1] + timings[n // 2]) / 2
        return timings[n // 2]

    def _calc_iqr(self) -> IQRValues:
        if not self._iqr_values:
            timings = sorted(self.timings)
            n = len(timings)
            q1 = timings[n // 4]
            q3 = timings[3 * n // 4]
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            self._iqr_values = IQRValues(
                q1=q1,
                q3=q3,
                iqr=iqr,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
            )
        return self._iqr_values

    @property
    def q1(self) -> float:
        return self._calc_iqr().q1

    @property
    def q3(self) -> float:
        return self._calc_iqr().q3

    @property
    def iqr(self) -> float:
        return self._calc_iqr().iqr

    @property
    def ops(self) -> float:
        return 1.0 / self.min if self.min > 0 else 0.0

    @property
    def ops_rel(self) -> float:
        return self.sample_size / self.min if self.min > 0 else 0.0

    @property
    def outliers(self) -> list[float]:
        """Return a list of timings that are considered outliers."""
        iqrv = self._calc_iqr()
        # https://en.wikipedia.org/wiki/Outlier
        # https://en.wikipedia.org/wiki/Interquartile_range
        return [x for x in self.timings if x < iqrv.lower_bound or x > iqrv.upper_bound]

    def slug(self) -> str:
        ctx = self.benchmark_manager.context
        v = ctx.project.version
        py = ctx.python.implementation_version(strip_patch=True)
        return sluggify(f"v{v}_{py}_{self.full_name}")

    def __enter__(self) -> Self:
        self.start_time = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.elap = time.monotonic() - self.start_time

    def loaded_state(self) -> dict[str, Any]:
        lctx = self.benchmark_manager.loaded_context

        res = {
            "name": self.name,
            "variant": self.variant,
            # "project": self.project,
            "python": self.python,
            "sample_size": self.sample_size,
        }
        res.update(lctx)
        return res

    def to_dict(self, add_meta: bool = True) -> dict[str, Any]:
        res = {
            "name": self.name,
            "variant": self.variant,
            "start_time": self.start_time,
            "elap": self.elap,
            "iterations": self.iterations,
            "sample_size": self.sample_size,
            "timings": self.timings,
        }
        if add_meta:
            ctx = self.benchmark_manager.context
            res.update(
                {
                    "python": ctx.python.version,
                    "project": ctx.project.name,
                    "version": ctx.project.version,
                    "debug_mode": ctx.python.debug_mode,
                    "hardware": ctx.hw.slug(),
                    "system": ctx.os.slug(),
                    "client": ctx.client_slug(),
                    "tag": self.benchmark_manager.tag,
                }
            )
        return res

    def save(self):
        folder = self.benchmark_manager.folder
        path = folder / f"{self.slug()}.bmr.json"
        _ = path.exists()
        with path.open("w") as f:
            json_dump(self.to_dict(), f, pretty=True)

    @classmethod
    def from_dict(cls, bm: BenchmarkManager, item: dict[str, Any]) -> Self:
        self = cls(bm, item["name"], variant=item.get("variant", ""))
        self.start_time = item["start_time"]
        self.timings = item["timings"]
        self.sample_size = item["sample_size"]
        self.iterations = item["iterations"]
        self.python = item["python"]
        self.variant = item["variant"]
        return self


class BenchmarkRunner:
    """Define default arguments for subsequent calls to `.run()`."""

    def __init__(
        self,
        *,
        bm: BenchmarkManager | None = None,
        #: A name for this benchmark run.
        name: str,
        #: A variant name for this benchmark run.
        variant: str = "",
        #: A setup statement to execute before the main statement (not timed).
        setup: str = "pass",
        #: Verbosity level (0: quiet, 1: normal, 2: verbose)
        verbose: int = 0,
        #: Number of times to repeat the test.
        repeat: int = 5,
        #: Number of loops to run. If 0, `timeit` will determine the iterations
        #: automatically.
        iterations: int = 0,
        #:
        sample_size: int = 1,
        #: A dict containing the global variables.
        globals: dict[str, Any] | None = None,
        #: Use `time.process_time` instead of `time.monotonic` for measuring CPU time.
        process_time: bool = False,
        #: A group name for this benchmark run.
        group: str = "",
        #: Save results to disk.
        save_results: bool = True,
    ):
        self.run_list: list[Benchmark] = []
        self.benchmark_manager = bm or BenchmarkManager.singleton()
        self.name = name
        self.variant = variant
        self.setup = setup
        self.verbose = verbose
        self.repeat = repeat
        self.iterations = iterations
        self.sample_size = sample_size
        self.globals = globals
        self.process_time = process_time
        self.group = group
        self.save_results = save_results

    def run(
        self,
        stmt: str,
        *,
        variant: str,
        setup: str | None = None,
        verbose: int | None = None,
        repeat: int | None = None,
        iterations: int | None = None,
        sample_size: int | None = None,
        globals: dict[str, Any] | None = None,
        process_time: bool | None = None,
        group: str | None = None,
        save_results: bool | None = None,
    ):
        bm = self.benchmark_manager
        res = bm.run_timings(
            name=self.name,
            stmt=stmt,
            variant=variant,
            setup=setup if setup is not None else self.setup,
            verbose=verbose if verbose is not None else self.verbose,
            repeat=repeat if repeat is not None else self.repeat,
            iterations=iterations if iterations is not None else self.iterations,
            sample_size=sample_size if sample_size is not None else self.sample_size,
            globals=globals if globals is not None else self.globals,
            process_time=process_time
            if process_time is not None
            else self.process_time,
            group=group if group is not None else self.group,
            save_results=save_results
            if save_results is not None
            else self.save_results,
        )
        self.run_list.append(res)

    def print(self):
        print(f"BenchmarkRunner: {self.name}")  # noqa: T201
        for i, benchmark in enumerate(sorted(self.run_list), 1):
            print(f"  {i}: {benchmark}")  # noqa: T201


class BenchmarkManager:
    """Manage a suite of multiple benchmarks."""

    # DEFAULT_OPTIONS = {
    #     "results_file": "benchman-results.json",
    # }

    def __init__(self, *, path: Path | str | None = None, create_folder=True) -> None:
        #: The context for this benchmark run.
        self.context = BaseContextInfo(path=path)
        #: A tag for this benchmark run (optional, defaults to None).
        self.tag: str = "latest"
        #:
        self.combine_date: str | None = None
        #:
        self.loaded_context: dict[str, Any] = {}
        #: A list of all benchmarks, grouped by group name.
        self.benchmarks: dict[str, list[Benchmark]] = {"": []}

        self.folder: Path = self.context.project.root_folder / ".benchman"
        if create_folder:
            self.folder.mkdir(parents=False, exist_ok=True)

        # Load options from pyproject.toml `[tool.benchman]`
        self.options: dict[str, Any] = {}
        pyproject_toml = self.context.project.pyproject_toml
        if pyproject_toml:
            self.options.update(pyproject_toml.get("tool", {}).get("benchman", {}))

        #: self.timer = timing.
        self.timer = timeit.default_timer
        # if process_time:
        #     self.timer = time.process_time

        # pprint.pprint(self.context.to_dict())
        return

    def __repr__(self):
        return (
            f"{self.__class__.__name__}<{self.context}, "
            f"n={len(list(self.iter_benchmarks()))}>"
        )

    def count(self):
        return len(list(self.iter_benchmarks()))

    _global_benchman: Self | None = None

    @classmethod
    def singleton(cls) -> Self:
        """Return the global `BenchmarkManager` instance."""
        if cls._global_benchman is None:
            cls._global_benchman = cls()
        assert cls._global_benchman
        return cast(Self, cls._global_benchman)

    @property
    def project_name(self) -> str:
        return self.context.project.name

    @property
    def project_version(self) -> str:
        return self.context.project.version

    def make_slug(self, *, tag: str | None = None) -> str:
        sl = [
            self.project_name,
            self.context.client_slug(),
        ]
        if not tag:
            tag = "latest"

        if tag in ("base", "latest"):
            # pv = self.project_version.replace(".", "_")
            # sl.append(f"v{pv}_{tag}")
            sl.append(tag)
        elif tag:
            sl.append(tag)

        return ".".join(sl)

    def iter_benchmarks(
        self, *, group: str | None = None, name: str | None = None
    ) -> Iterator[Benchmark]:
        if group is None:
            assert name is None
            for _group, benchmarks in self.benchmarks.items():
                yield from benchmarks
        elif name:
            for bench in self.benchmarks.get(group, []):
                if bench.name == name:
                    yield bench
        else:
            yield from self.benchmarks.get(group, [])

    def get_best(
        self, *, group: str | None = None, name: str | None = None
    ) -> Benchmark | None:
        """Return the benchmark with the best runtime."""
        assert self.benchmarks
        best: Benchmark | None = None
        for b in self.iter_benchmarks(group=group, name=name):
            if not best or b.min < best.min:
                best = b
        return best

    def get_best_time_unit(
        self, *, group: str | None = None, name: str | None = None
    ) -> TTimeUnit:
        """Return the time unit of the benchmark with the best runtime."""
        best = self.get_best(group=group, name=name)
        if best is None:
            return "sec"
        ts = get_time_unit(best.min)
        return ts.unit

    def _path_and_prefix(self, *, group: str) -> tuple[Path, str]:
        path = self.folder / ".benchman" / self.context.slug()
        prefix = "$".join([group])
        return path, prefix

    def add_benchmark(self, benchmark: Benchmark, *, group: str = "") -> None:
        if group not in self.benchmarks:
            self.benchmarks[group] = []
        self.benchmarks[group].append(benchmark)

    # def save(self):
    #     pass

    @classmethod
    def load(cls, path: Path | str) -> Self:
        path = Path(path)
        if not path.is_file():
            raise FileNotFoundError(path)

        self = cls(path=path.parent, create_folder=False)

        with path.open("r") as f:
            content = json.load(f)
        self.tag = content.get("tag", "latest")
        self.combine_date = content.get("combine_date", None)
        self.loaded_context = content["context"]

        for item in content["data"]:
            bmr = Benchmark.from_dict(self, item)

            self.add_benchmark(bmr)
        return self

    def compare_results(self, other):
        pass

    def format_results(self) -> list[str]:
        results = []
        # Sort by group name
        for group, benchmarks in self.benchmarks.items():
            results.append(f"Group: {group or 'default'}")
            # TODO: use get_best_time_unit() to unify unit for the group?
            # Sort by best time
            for i, benchmark in enumerate(sorted(benchmarks), 1):
                results.append(f"  {i}: {benchmark}")
                # ol = benchmark.outliers
                # results.append(f"  {i}: {benchmark}, {len(ol)} outliers")

        return results

    def print_results(self):
        for line in self.format_results():
            print(line)  # noqa: T201

    def run_timings(
        self,
        #: A name for this benchmark run.
        name: str,
        *,
        #: The statement to be timed.
        stmt: str,
        #: A variant name for this benchmark run.
        variant: str = "",
        #: A setup statement to execute before the main statement (not timed).
        setup: str = "pass",
        #: Verbosity level (0: quiet, 1: normal, 2: verbose)
        verbose: int = 0,
        #: Number of times to repeat the test.
        repeat: int = 5,
        #: Number of loops to run. If 0, `timeit` will determine the iterations
        #: automatically.
        iterations: int = 0,
        #:
        sample_size: int = 1,
        #: A dict containing the global variables.
        globals: dict[str, Any] | None = None,
        #: Use `time.process_time` instead of `time.monotonic` for measuring CPU time.
        process_time: bool = False,
        #: A group name for this benchmark run.
        group: str = "",
        #: Save results to disk.
        save_results: bool = True,
    ) -> Benchmark:
        """Run `stmt` in a loop and return a `BenchmarkRun` object."""
        if self.context.python.debug_mode:
            warnings.warn(
                "Application is running in debug mode. "
                "This may be due coverage, a debugger or other instrumentation. "
                "Performance timings may be affected!",
                stacklevel=2,
            )

        start: float = time.monotonic()
        res: TimingsResult = run_timings(
            name=name,
            stmt=stmt,
            setup=setup,
            verbose=verbose,
            repeat=repeat,
            iterations=iterations,
            globals=globals,
            process_time=process_time,
        )
        elap = time.monotonic() - start

        benchmark = Benchmark(self, name, variant=variant)
        benchmark.start_time = start
        benchmark.elap = elap
        benchmark.iterations = res.iterations
        benchmark.sample_size = sample_size
        benchmark.timings = res.timings.copy()

        self.add_benchmark(benchmark, group=group)
        if save_results:
            benchmark.save()
        return benchmark

    def report(self, format: str = "terminal") -> None:
        self.print_results()

    def make_runner(
        self,
        *,
        name: str,
        variant: str = "",
        setup: str = "pass",
        verbose: int = 0,
        repeat: int = 5,
        iterations: int = 0,
        sample_size: int = 1,
        globals: dict[str, Any] | None = None,
        process_time: bool = False,
        group: str = "",
        save_results: bool = True,
    ):
        bmr = BenchmarkRunner(
            bm=self,
            name=name,
            variant=variant,
            setup=setup,
            verbose=verbose,
            repeat=repeat,
            iterations=iterations,
            sample_size=sample_size,
            globals=globals,
            process_time=process_time,
            group=group,
            save_results=save_results,
        )
        return bmr
