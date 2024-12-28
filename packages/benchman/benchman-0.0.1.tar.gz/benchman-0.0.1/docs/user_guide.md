# BenchMan
> Benchmark manager

## Glossaary
- group
- name
- variant
- iterations (also number)
- round (also loop, repeat)
- Benchmark
- sample_size
- dimension
- metric
- dynamic column
- warmup
- client

### Metrics
- `min`: seconds per iteration (best reslt of all measured rounds)
- 'ops': operations per second (calulted as `1.0 / min`)
- ...

## Features

1. Run a code snippet, method, or any command line script and measure the
   time. Auto-scale the number of iterations and repeat the loop multiple 
   times to calculate deviation and other metrics.

2. Integrate with [pytest](https://docs.pytest.org/en/stable/) and 
   [tox](https://tox.wiki/) for easy excution of benchmarks in multiple
   Python environments.

3. Store single benchmark results in a single file and add context meta data
   for later reference and comparison.

4. Transform, sort, filter, and aggregate the benchmark results.

5. Generate reports in multiple formats.


## Concept

If for example, we want to measure the performance of a quick-sort method, we 
will call the test in a loop with a large number of *iterations*, 
like 1,000 times, and measure the elapsed time. <br>
The number of iterations depends on the execution time. 
Typically we chose a number that results in an execution time of 0.2 to 1.0 
seconds. 'Auto-scaling' helps to find this number automatically. <br>
Running the test in 1,000 iterations, we call one *round*. <br>
We divide the elapsed time by the iteration count, giving us
_seconds per iteration_ as float value.

We then repeat 1,000 iterations in several *rounds*, for example five times. 
The whole *benchmark* will take 5 x 0.2 .. 1.0 seconds, so about one to five 
seconds in total.

After that, we have five different float values for _seconds per iteration_.
For this values we can calculate statistics like min, max, mean, standard deviation,
median, interquartile range (IQR), oprations per second (OPS, calculated as 
*iteration count* / *min*).

In order to compare quick-sort with bubble-sort and insertion-sort...

Compare , i.e. the behavior of sorting algorithms in relation to
the data sample size
small, medium, large -> sample_size = 10, 100, 1000

We should interpret statistical metrics with care though. 
From the Python `timeit` standard module:

> Note: it's tempting to calculate mean and standard deviation
> from the result vector and report these.  However, this is not
> very useful.  In a typical case, the lowest value gives a
> lower bound for how fast your machine can run the given code
> snippet; higher values in the result vector are typically not
> caused by variability in Python's speed, but by other
> processes interfering with your timing accuracy.  So the min()
> of the result is probably the only number you should be
> interested in.  After that, you should look at the entire
> vector and apply common sense rather than statistics.

## Install


`.gitignore`:
```
...
.benchman/
```


## Integrate with Pytest

`.conftest.py`:
```py
import sys

import pytest
from benchman import BenchmarkManager


def pytest_addoption(parser) -> None:
    """Add an optional command line arguments to pytest.

    This `--benchmarks` flag is then used to enable benchmarks using the
    `@benchmark` decorator.
    """
    parser.addoption("--benchmarks", action="store_true")


#: '@benchmark' decorator to skip test unless `--benchmarks` is set.
benchmark = pytest.mark.skipif(
    "--benchmarks" not in sys.argv,
    reason="`--benchmarks` not set",
)


#: Define a fixture to provide a singleton instance of the BenchmarkManager.
#: This uses dependency injection to provide the `benchman` fixture to tests.
@pytest.fixture(scope="session")
def benchman() -> BenchmarkManager:
    return BenchmarkManager.singleton()
```

## Integrate with Tox

```bash
tox -c tox_benchmarks.ini --parallel 
```

`tox_benchmarks.ini`:
```in[tox]
basepython = python3.12
envlist =
    py{39,310,311,312,313}
    benchman-combine
skip_missing_interpreters = true


[testenv]
deps =
    pytest
changedir = {toxinidir}
commands =
    python -V
    pytest -v -o addopts="" --benchmarks tests


[testenv:benchman-combine]
description = Combine benchmark results
# Make sure to run this last
depends =  py{39,310,311,312,313}
changedir = {toxinidir}
commands:
    benchman combine 
    benchman report
    benchman report --output .benchman/report.latest.md

```