"""Convert Datasets into human-readable representation."""

from abc import ABC, abstractmethod
from io import TextIOBase
from pathlib import Path

import tablib

from benchman.dataset import DataCell, Dataset
from benchman.util import DEFAULT_TIME_SCALE, FileOrStdout, TLegendLines, logger


class Reporter(ABC):
    """Abstract class for reporting Datasets."""

    def __init__(self, dataset: Dataset):
        self.dataset: Dataset = dataset

    @abstractmethod
    def report(self, *, out: Path | str | TextIOBase | None, **kwargs) -> None:
        """Return a human-readable representation of the Dataset."""

    def get_description_info(self) -> dict[str, str | TLegendLines]:
        return self.dataset.get_description_info()

    def _format_cell(self, cell: DataCell) -> str | int | float | None:
        """Return a string representation of the classes."""
        dataset = cell.dataset
        col_info = cell.col_info

        value = cell.value
        ts = DEFAULT_TIME_SCALE
        if isinstance(value, int):
            value = f"{value:,}"
        elif col_info.unit in ("s", "1/s"):
            assert isinstance(value, float), (value, cell)
            ts, ts_ops = dataset.time_scale_by_benchmark_name[cell.benchmark.name]
            if col_info.unit == "s":
                value = ts.format_seconds(value)
            else:
                value = ts_ops.format_rate(value)

        if cell.dataset.time_scale_by_benchmark_name:
            return value

        # return f" ({','.join(classes)})"
        cl = []
        for c in cell.classes:
            s = ""
            if c.startswith("name-"):
                s += "n"
                # continue
            elif c.startswith("variant-"):
                s += "v"
                continue
            elif c.startswith("row-"):
                s += "r"

            if c.endswith("-best"):
                s += "++"
            elif c.endswith("-good"):
                s += "+"
            elif c.endswith("-bad"):
                s += "-"
            elif c.endswith("-worst"):
                s += "--"

            if s:
                cl.append(s)

        if cl:
            return f' ({",".join(cl)})'
        return ""

    def to_tablib(self) -> tablib.Dataset:
        tds = tablib.Dataset(
            title=self.dataset.name,
            headers=self.dataset.header_titles,
        )
        for row in self.dataset.rows:
            cells = [self._format_cell(c) for c in row]
            # cells = [f"{c.value} ({','.join(c.classes)})" for c in row]
            # cells = [c.value for c in row]
            try:
                tds.append(cells)
            except Exception as e:
                logger.error(f"Error {e!r} adding row: {cells}")
                logger.error(f"{tds.headers=}")
                raise
        return tds


class TablibReporter(Reporter):
    """Text representation of a Dataset."""

    # See https://tablib.readthedocs.io/en/stable/formats.html
    # fmt: off
    cli_formats = [
        "fancy_grid", "github", "grid", "html", "jira", "latex_booktabs", 
        "latex_raw", "latex", "mediawiki", "moinmoin", "orgtbl", "pipe", "plain", 
        "presto", "psql", "rst", "simple", "textile", "tsv", "youtrack",
    ]
    format_map = {
        "html": "cli.html",
        "markdown": "cli.pipe",
        "csv": "cli.csv",
        "json": "cli.json",
        "yaml": "cli.yaml",
        "df": "cli.df",
    }
    # fmt: on

    def report(
        self,
        *,
        format: str = "cli.pipe",
        out: Path | str | TextIOBase | None = None,
        **kwargs,
    ) -> None:
        """Write a human-readable representation of the Dataset.

        The heavy lifting is done by `tablib.Dataset.export()`.
        """
        format = self.format_map.get(format, format)

        export, format = format.split(".", 1)

        assert export == "cli", f"Invalid format: {format}"
        assert format in self.cli_formats, f"Invalid cli format: {format}"

        info = self.get_description_info()

        tds = self.to_tablib()

        if isinstance(out, (Path, str)):
            logger.info(f"Writing to {Path(out).absolute()}")

        with FileOrStdout(out) as file:

            def wl(s: str = "") -> None:
                file.write(f"{s}\n")

            def wl2(lines: str | list = "", *, prefix="") -> None:
                if not lines:
                    return
                if isinstance(lines, str):
                    lines = [lines]
                for s in lines:
                    if isinstance(s, tuple):
                        file.write(f"{prefix}{s[0]}: {s[1]}\n")
                    else:
                        file.write(f"{prefix}{s}\n")
                return

            # wl(f"\n# {info["title"]}")
            wl2(info["title"], prefix="# ")

            # if info["subtitle"]:
            #     wl("\n> " + "\n> ".join(info["subtitle"]))
            wl2(info["subtitle"], prefix="\n> ")
            wl()

            # The table itself:
            wl(str(tds.export(export, tablefmt=format)))

            wl()
            wl2(info["legend"])
            wl()
            wl2(info["warnings"])
            wl()
            # for s in info["legend"]:
            #     wl(s)

            # for s in info["warnings"] or []:
            #     wl(s)
            wl()
