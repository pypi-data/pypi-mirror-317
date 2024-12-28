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
