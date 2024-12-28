# (c) 2024 Martin Wendt; see https://github.com/mar10/benchman
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
""" """

# NO_ruff: noqa: T201, T203 `print` found

from __future__ import annotations

import datetime
import platform
import socket
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psutil
from typing_extensions import Self

from .util import get_machine_id, get_project_info, hash_string, sluggify


@dataclass
class HWInfo:
    cpu: str
    ram: str
    machine: str
    machine_id: str
    mac: str
    # gpu: str

    def slug(self) -> str:
        return sluggify(f"{self.machine}_{self.ram}")

    def to_dict(self) -> dict[str, Any]:
        return {"cpu": self.cpu, "ram": self.ram, "machine": self.machine}

    @classmethod
    def create(cls) -> Self:
        ram_info = f"{round(psutil.virtual_memory().total / (1024 ** 3))} GB"
        # gpu_info = None  # This would require a library like GPUtil to get dynamically

        return cls(
            cpu=platform.processor(),
            ram=ram_info,
            machine=platform.machine(),
            machine_id=get_machine_id(),
            mac=str(uuid.getnode()),
            # gpu=gpu_info,
        )


@dataclass
class ProjectInfo:
    name: str
    version: str
    root_folder: Path
    pyproject_toml: dict | None = None

    def slug(self) -> str:
        return sluggify(f"v{self.version}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "root_folder": str(self.root_folder),
        }

    @classmethod
    def create(
        cls,
        *,
        path: Path | str | None = None,
    ) -> Self:
        # Check if we are running from a project folder
        if path is None:
            path = Path.cwd()
        else:
            path = Path(path)
        info = get_project_info(path)
        project_root = info["project_root"]
        project_name = info["project_name"]
        project_version = info["project_version"]
        pyproject_toml = info["pyproject_toml"]

        project_info = cls(
            root_folder=project_root,
            name=project_name,
            version=project_version,
        )
        project_info.pyproject_toml = pyproject_toml
        return project_info


@dataclass
class OSInfo:
    name: str
    version: str

    def slug(self) -> str:
        return sluggify(f"{self.name}_{self.version}")

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "version": self.version}

    @property
    def is_windows(self) -> bool:
        return self.name == "Windows"

    @classmethod
    def create(cls) -> Self:
        uname = platform.uname()
        name = platform.system()
        version = uname.release  # latform.version()
        return cls(name=name, version=version)


@dataclass
class PythonInfo:
    version: str
    implementation: str
    compiler: str
    build: str
    debug_mode: bool
    optimized: bool

    def slug(self) -> str:
        # return sluggify(f"Py{self.version}")
        return sluggify(f"{self.implementation}_{self.version}")

    def implementation_version(self, *, strip_patch=False) -> str:
        v = self.version
        impl = self.implementation
        if impl == "CPython":  # 'CPython 3.9.7' -> 'Py39'
            if strip_patch:
                v = "".join(v.split(".")[:2])
            impl = "Py"
        else:
            impl += " "
        return f"{impl}{v}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "implementation": self.implementation,
            "compiler": self.compiler,
            "build": self.build,
        }

    @classmethod
    def create(cls) -> PythonInfo:
        version = platform.python_version()
        implementation = platform.python_implementation()
        compiler = platform.python_compiler()
        build = platform.python_build()[0]
        debug_mode = bool(getattr(sys, "gettrace", None) and sys.gettrace())
        return cls(
            version=version,
            implementation=implementation,
            compiler=compiler,
            build=build,
            debug_mode=debug_mode,
            optimized=not sys.flags.debug,
        )


# @singleton
class BaseContextInfo:
    """
    Runtime context information about the client system (constant).
    """

    def __init__(
        self,
        *,
        path: Path | str | None = None,
    ) -> None:
        self.hostname = socket.gethostname()
        self.date = datetime.datetime.now(datetime.timezone.utc)
        self.python: PythonInfo = PythonInfo.create()
        self.os: OSInfo = OSInfo.create()
        self.hw: HWInfo = HWInfo.create()
        self.project: ProjectInfo = ProjectInfo.create(path=path)

    def __repr__(self):
        uname = platform.uname()
        return "{}<node: {!r}, os: {} {}, machine: {}>".format(  # noqa: UP032
            self.__class__.__name__,
            uname.node,
            uname.system,
            uname.release,
            uname.machine,
        )

    def client_slug(self) -> str:
        """Identifies the current client system."""
        # return hash_string(self.hw.mac, length=8)
        # return self.hw.mac
        # return hash_string(platform.node() + "_" + str(platform.uname()))
        return hash_string(self.hw.machine_id)

    def slug(self) -> str:
        return sluggify(
            "~".join(
                [
                    self.project.slug(),
                    self.python.slug(),
                    self.date.strftime("%Y%m%d"),
                    self.hostname,
                    self.hw.slug(),
                    self.os.slug(),
                ]
            )
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "slug": self.slug(),
            "date": self.date.isoformat(),
            "hostname": self.hostname,
            "python": self.python.to_dict(),
            "os": self.os.to_dict(),
            "hw": self.hw.to_dict(),
            "project": self.project.to_dict(),
        }
