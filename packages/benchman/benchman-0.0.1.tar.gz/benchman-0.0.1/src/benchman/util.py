# (c) 2024 Martin Wendt; see https://github.com/mar10/benchman
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import logging
import operator
import os
import re
import shutil
import subprocess
import sys
import threading
import uuid
from dataclasses import dataclass
from io import TextIOBase
from pathlib import Path
from typing import Any, Union, cast

import build.util
import toml
from typing_extensions import Literal

logger = logging.getLogger("benchman")

PYTHON_VERSION = f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"

TLegendLines = list[Union[str, tuple[str, str]]]
# TLegendLines2 = list[Union[str, tuple[str, str]]]

TTimeUnit = Literal["femto", "pico", "nano", "micro", "milli", "sec"]
# TTimeUnit2 = Literal["femto", "pico", "nano", "micro", "milli", "sec"]


@dataclass
class TimeScale:
    scale: float
    unit: TTimeUnit
    name: str
    short: str
    # precision: int = 3
    inv: str
    inv_short: str
    # inv_scale: float = 1.0
    # inv_precision: int = 3  #

    def format_seconds(self, seconds: float, *, precision: int = 0) -> str:
        secs = seconds / self.scale
        return f"{secs:,.{precision}f} {self.short}"

    def format_rate(self, seconds: float, *, precision: int = 3) -> str:
        secs = seconds * self.scale
        return f"{secs:,.{precision}f} {self.inv_short}"


TIME_SCALE_LIST = [
    TimeScale(1e-15, "femto", "femtosecond", "fs", "Peta", "P"),
    TimeScale(1e-12, "pico", "picosecond", "ps", "Tera", "T"),
    TimeScale(1e-9, "nano", "nanosecond", "ns", "Giga", "G"),
    TimeScale(1e-6, "micro", "microsecond", "μs", "Mega", "M"),
    TimeScale(1e-3, "milli", "millisecond", "ms", "kilo", "k"),
    TimeScale(1.0, "sec", "second", "s", "", ""),
]
TIME_SCALE_MAP = {ts.unit: ts for ts in TIME_SCALE_LIST}
DEFAULT_TIME_SCALE = TIME_SCALE_MAP["sec"]

_time_scale_ramp: list[tuple[float, TimeScale]] = sorted(
    [(ts.scale, ts) for ts in TIME_SCALE_LIST], reverse=True
)


def get_time_unit(seconds: float) -> TimeScale:
    for scale, unit in _time_scale_ramp:
        if seconds >= scale:
            return unit
    return DEFAULT_TIME_SCALE


def find_project_root(start_path: str | Path | None = None) -> Path | None:
    """Find the root folder of the current project."""
    root: Path | None = None
    try:
        logger.debug("Looking for Git repository...")
        # Run 'git rev-parse' to find the top-level directory
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        root = Path(git_root)
        logger.debug(f"Git repository found: {root}")
    except subprocess.CalledProcessError:
        # Not a Git repository
        logger.debug(
            "No Git repository found, looking for pyproject.toml or setup.py..."
        )

    if root is None:
        # Search parent folders for pyproject.toml or setup.py
        # Start from the current working directory if not specified
        current_path = Path(start_path or os.getcwd()) / "dummy-file.txt"
        for parent in current_path.parents:
            logger.debug(f"Checking {parent}...")
            # Look for a defining file, such as 'pyproject.toml' or '.git'
            if (
                (parent / "pyproject.toml").exists()
                or (parent / "setup.py").exists()
                or (parent / ".git").exists()
            ):
                root = parent
    return root


_project_info = None


def get_project_info(path: Path | None = None) -> dict[str, Any]:
    global _project_info

    if _project_info is not None:
        return _project_info

    project_root = find_project_root(path)
    # logger.log(logging.WARNING, f"Project root: {project_root}", stack_info=True)

    if project_root is None:
        raise FileNotFoundError(f"Project root not found in {path} or parent folders")

    if (project_root / "pyproject.toml").is_file():
        with open(project_root / "pyproject.toml") as f:
            pyproject_toml = toml.load(f)
        if "project" in pyproject_toml:
            project_name: str = pyproject_toml["project"]["name"]
        else:
            logger.warning(
                "pyproject.toml does not contain a [project] section "
                "(trying setup.cfg)..."
            )

            wm = build.util.project_wheel_metadata(project_root)
            pn = wm.get("name")
            assert pn
            project_name = pn

            # from setuptools.config import read_configuration

            # conf_dict = read_configuration(project_root / "setup.cfg")
            # project_name = conf_dict["metadata"]["name"]

    else:  # setup.py
        raise FileNotFoundError(f"pyproject.toml not found in {project_root}")

    # Get the project version from the installed package metadata
    project_version = importlib.metadata.version(project_name)
    # Get the project name again, because it might be different from the package name
    meta = importlib.metadata.metadata(project_name)
    project_name = meta["Name"]

    _project_info = {
        "project_name": project_name,
        "project_version": project_version,
        "project_root": project_root,
        "pyproject_toml": pyproject_toml,
    }
    return _project_info


# PROJECT_ROOT: Path = find_project_root()


class BenchmarkSuiteFile:
    def __init__(self, path: Path | str):
        self.path = Path(path)
        file_name = self.path.name
        if not file_name.endswith(".bench.json"):
            raise ValueError(f"Invalid file name: {self.path}")
        file_name = file_name[:-11]
        self.project, self.client_id, self.tag = file_name.split(".", 2)

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.path}>"

    def __str__(self):
        return str(self.path)

    @property
    def name(self) -> str:
        return self.path.name

    def _read(self):
        with self.path.open("r") as f:
            return json.load(f)

    def _patch(self, json: dict, keep_date: bool = False):
        mdate = self.path.stat().st_mtime
        with self.path.open("w") as f:
            json_dump(json, f, pretty=True)
        if keep_date:
            os.utime(self.path, (mdate, mdate))

    def save_tag(
        self, new_tag: str, *, replace: bool, keep_time: bool = False
    ) -> BenchmarkSuiteFile:
        """Save the benchmark file with a new tag (filename and json data).

        If `replace` is True, this original file is replaced with the new tag.
        Otherwise, a new file is created with the new tag and returned.

        If `keep_time` is True, the original file's modification time is preserved.
        """
        if self.tag == new_tag:
            raise ValueError(f"Tag is already '{new_tag}'")

        new_path = self.path.with_name(
            f"{self.project}.{self.client_id}.{new_tag}.bench.json"
        )
        if replace:
            result = self
            self.tag = new_tag
            self.path.replace(new_path)
            self.path = new_path
            logger.info(f"Renamed {self.path} to {new_path.name}")
        else:
            shutil.copy(self.path, new_path)
            result = BenchmarkSuiteFile(new_path)
            logger.info(f"Copied {self.path} to {new_path.name}")
        data = result._read()
        data["tag"] = new_tag
        result._patch(data, keep_date=keep_time)
        return result

    @classmethod
    def find_files(cls, folder: Path | str) -> list[BenchmarkSuiteFile]:
        folder = Path(folder)
        return [cls(p) for p in folder.glob("*.bench.json")]


def is_running_on_ci() -> bool:
    return bool(os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"))


def extract_items(
    d: dict[str, Any], keys: list[str], *, remove: bool = False
) -> dict[str, Any]:
    """Create a subset of a dictionary by extracting specific keys.

    Args:
        d (dict): The source dictionary.
        keys (list): The keys to extract.
        remove (bool): If True, the keys are removed from the source dictionary.
    """
    if remove:
        return {k: d.pop(k, None) for k in keys if k in d}
    return {k: d[k] for k in keys if k in d}


def json_dump(data: Any, file: TextIOBase, *, pretty: bool) -> None:
    """Write data to a file in JSON format, compact or pretty."""
    if pretty:
        json.dump(data, file, indent=2, separators=(",", ": "), sort_keys=True)
    else:
        json.dump(data, file, indent=0, separators=(",", ":"), sort_keys=True)


class FileOrStdout:
    def __init__(self, out: Union[Path, str, TextIOBase, None] = None):
        self.out = out
        self.file: TextIOBase | None = None

    def __enter__(self) -> TextIOBase:
        if self.out is None:
            self.file = cast(TextIOBase, sys.stdout)
        elif isinstance(self.out, TextIOBase):
            self.file = self.out
        else:
            self.file = open(self.out, "w")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.file is not sys.stdout and self.file is not None:
            self.file.close()


class ExpressionFilter:
    """Filter a list of objects based on a rule string.

    Attribute Comparison: attribute operator value
    Logical AND: Separate conditions with a comma `,`
    Logical OR: Separate conditions with a semicolon `;`
    Example Syntax:
    "name eq alice, age gt 20": Logical AND, matches objects where name is alice
                                and age is greater than 20.
    "name eq alice; age gt 20": Logical OR, matches objects where name is alice
                                or age is greater than 20.

    Supported Operators:
        eq: Equal to
        ne: Not equal to
        gt: Greater than
        ge: Greater than or equal to
        lt: Less than
        le: Less than or equal to
        *=: Contains
        ^=: Starts with

    Args:
        objects (list[Any]): _description_
        rule (str): _description_

    Returns:
        list[Any]: _description_
    """

    ops = {
        "!=": operator.ne,
        "*=": operator.contains,
        "!*": lambda a, b: not operator.contains(a, b),
        "^=": lambda a, b: str(a).startswith(str(b)),
        "!^": lambda a, b: not str(a).startswith(str(b)),
        "<": operator.lt,
        "<=": operator.le,
        "<>": operator.ne,
        "==": operator.eq,
        ">": operator.gt,
        ">=": operator.ge,
        "eq": operator.eq,
        "ge": operator.ge,
        "gt": operator.gt,
        "le": operator.le,
        "lt": operator.lt,
    }

    def __init__(self, rule: str):
        self.rule = rule
        self.conditions = self._parse_rule()

    def __repr__(self):
        return f"self.__class__.__name__<{self.rule}>"

    def _parse_rule(self) -> list[tuple]:
        conditions = []
        for cond in self.rule.split(","):
            attr, op, svalue = cond.strip().split()
            value: str | float = svalue
            try:
                value = float(svalue)
            except ValueError:
                pass
            conditions.append((attr, self.ops[op], value))
        return conditions

    def matches(self, obj: Any) -> bool:
        return all(op(getattr(obj, attr), value) for attr, op, value in self.conditions)

    def filter(self, object_list: list[Any]) -> list[Any]:
        return [obj for obj in object_list if self.matches(obj)]


def filter_objects(objects: list[Any], rule: str) -> list[Any]:
    """Filter a list of objects based on a rule string."""
    ef = ExpressionFilter(rule)
    return ef.filter(object_list=objects)


def split_tokens(s: str) -> list[str]:
    """Split a comma separated string into tokens, removing whitespace."""
    return [s.strip() for s in s.split(",")]


def singleton(cls):
    """
    A thread-safe decorator to ensure a class follows the Singleton
    design pattern.

    This decorator allows a class to have only one instance throughout
    the application. If the instance does not exist, it will create one;
    otherwise, it will return the existing instance. This implementation
    is thread-safe, ensuring that only one instance is created even in
    multithreaded environments.

    :param: cls (type): The class to be decorated as a Singleton.
    :return: function: A function that returns the single instance of the
             class.
    """
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs) -> object:
        """
        Return a single instance of the decorated class, creating it
        if necessary.

        This function ensures that only one instance of the class exists.
        It uses a thread-safe approach to check if an instance of the class
        already exists in the `instances` dictionary. If it does not exist,
        it creates a new instance with the provided arguments. If it does
        exist, it returns the existing instance.

        :param: *args: Variable length argument list for the class constructor.
        :param: **kwargs: Arbitrary keyword arguments for the class constructor.
        :return: object: The single instance of the class.
        """
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]

    return get_instance


allowed_slug = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.~()"
)


def sluggify(text: str) -> str:
    """
    Convert a string to a slug by replacing spaces with underscores and
    removing any non-alphanumeric characters.

    :param text: The input string to be converted to a slug.
    :return: str: The slug version of the input string.
    """
    return "".join(c if c in allowed_slug else "_" for c in text).strip("_.-~")


def hash_string(s: str, *, length: int = 16) -> str:
    """
    Calculate a hash value for a given string.

    :param s: The string to be hashed.
    :return: int: The hash value of the input string.
    """
    h = hashlib.sha256(s.encode()).hexdigest()
    if length <= len(h):
        return h[:length]  # Truncate to the desired length
    else:
        # If the length is greater than the hash, pad with zeros
        return (h + "0" * length)[:length]


def smart_sort_key(val) -> Any:
    """Sort by numeric parts and string parts (pass to `sort(key=...)`)."""
    # org_val = val
    if isinstance(val, str):
        parts = []
        # Split the string into numeric (include '.' and ',') and non-numeric parts
        for part in re.split(r"(\d[\d,]*)", val):
            # for part in re.split(r"(\d[\d,]*(?:\.\d+)?)", val):
            try:
                # discarding thousands separator
                part = int(part.replace(",", ""))
                # print("int", repr(part))
            except ValueError:
                pass
            parts.append(part)
        if len(parts) > 0:
            val = tuple(parts)

    # print("sort", org_val, val)
    return val


def calculate_q1_q2_q3(data: list[float]) -> tuple[float, float, float]:
    """Calculate the first, second, and third quartiles of a list of numbers."""
    data = sorted(data)
    n = len(data)
    q1 = data[n // 4]
    q2 = data[n // 2]
    q3 = data[(3 * n) // 4]
    return q1, q2, q3


def format_time(
    seconds: float,
    *,
    unit: Union[TTimeUnit, TimeScale, None] = None,
    precision: int = 3,
) -> str:
    if unit is None:
        ts = get_time_unit(seconds)
    elif not isinstance(unit, TimeScale):
        ts = TIME_SCALE_MAP[unit]
    else:
        ts = unit

    return "{secs:,.{prec}f} {unit}".format(
        prec=precision, secs=seconds / ts.scale, unit=ts.short
    )


def byte_number_string(
    number: float,
    thousands_sep: bool = True,
    partition: bool = True,
    base1024: bool = False,
    append_bytes: bool = False,
    prec: int = 3,
) -> str:
    """Convert bytes into human-readable representation."""
    magsuffix = ""
    bytesuffix = ""
    assert append_bytes in (False, True, "short", "iec")
    if partition:
        magnitude = 0
        if base1024:
            while number >= 1024:
                magnitude += 1
                #                 number = number >> 10
                number /= 1024.0
        else:
            while number >= 1000:
                magnitude += 1
                number /= 1000.0
        magsuffix = ["", "K", "M", "G", "T", "P"][magnitude]
        if magsuffix:
            magsuffix = " " + magsuffix

    if append_bytes:
        if append_bytes == "iec" and magsuffix:
            bytesuffix = "iB" if base1024 else "B"
        elif append_bytes == "short" and magsuffix:
            bytesuffix = "B"
        elif number == 1:
            bytesuffix = " Byte"
        else:
            bytesuffix = " Bytes"

    if thousands_sep and (number >= 1000 or magsuffix):
        # locale.setlocale(locale.LC_ALL, "")
        # TODO: make precision configurable
        if prec > 0:
            # fs = "%.{}f".format(prec)
            # snum = locale.format_string(fs, number, thousandsSep)
            snum = f"{number:,.{prec}g}"
        else:
            # snum = locale.format("%d", number, thousandsSep)
            snum = f"{number:,g}"
        # Some countries like france use non-breaking-space (hex=a0) as group-
        # seperator, that's not plain-ascii, so we have to replace the hex-byte
        # "a0" with hex-byte "20" (space)
        # snum = hexlify(snum).replace("a0", "20").decode("hex")
    else:
        snum = str(number)

    return f"{snum}{magsuffix}{bytesuffix}"


def get_machine_id() -> str:
    """Return a unique identifier for this machine."""
    # See https://stackoverflow.com/a/74058166/19166

    def run(cmd) -> Union[str, None]:
        try:
            return subprocess.run(
                cmd, shell=True, capture_output=True, check=True, encoding="utf-8"
            ).stdout.strip()
        except Exception:
            return None

    if sys.platform == "darwin":
        res = run(
            "ioreg -d2 -c IOPlatformExpertDevice "
            "| awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'"
        )
    elif sys.platform == "win32" or sys.platform == "cygwin" or sys.platform == "msys":
        res = run("wmic csproduct get uuid").split("\n")[2].strip()

    elif sys.platform.startswith("linux"):
        res = run("cat /var/lib/dbus/machine-id") or run("cat /etc/machine-id")

    elif sys.platform.startswith("openbsd") or sys.platform.startswith("freebsd"):
        res = run("cat /etc/hostid") or run("kenv -q smbios.system.uuid")

    return res or str(uuid.getnode())


# def calculate_precision_digits(value: float) -> int:
#     """
#     Calculate the reasonable number of precision digits after the comma for a
#     floating point number.

#     Args:
#         value (float): The floating point number.

#     Returns:
#         int: The number of precision digits after the comma.
#     """
#     if value == 0:
#         return 0
#     import math

#     magnitude = math.floor(math.log10(abs(value)))
#     return max(0, -magnitude + 1)
