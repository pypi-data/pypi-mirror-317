# (c) 2024 Martin Wendt; see https://github.com/mar10/benchman
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
from __future__ import annotations

import pprint
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any, Callable

from typing_extensions import Literal

from benchman import Benchmark, BenchmarkManager
from benchman.util import (
    ExpressionFilter,
    TimeScale,
    TLegendLines,
    calculate_q1_q2_q3,
    get_time_unit,
    logger,
    smart_sort_key,
    split_tokens,
)


@dataclass(frozen=True)
class ColumnInfo:
    id: str
    short: str
    title: str
    description: str
    unit: Literal["", "n", "s", "1/s"]
    #: If True, this column is a metric (e.g. min, max, mean)
    metric: bool
    #: If True, larger is better
    inverse: bool

    def __str__(self):
        return f"{self.id} ({self.short}): {self.title} ({self.description})"

    def __repr__(self):
        return f"col_info<{self.id}>"


COL_INFO_LIST = [
    #
    # --- Dynamic columns ---
    #
    # Properties that are known for every Benchmark instance.
    # However, the values can occur more than once in a benchmark suite.
    # These can be used as row headers or dynamic columns in a dataset.
    #
    ColumnInfo("project", "Project", "Project", "Project name", "", False, False),
    ColumnInfo("version", "ver", "Proj. Ver", "Project version", "", False, False),
    ColumnInfo("tag", "Tag", "Tag", "Benchmark tag", "", False, False),
    ColumnInfo(
        "full_name",
        "Benchmark",
        "Full Name",
        "Full benchmark name (name, variant, sample size)",
        "",
        False,
        False,
    ),
    ColumnInfo("name", "Name", "Name", "Short benchmark name", "", False, False),
    ColumnInfo("variant", "Variant", "Variant", "Benchmark variant", "", False, False),
    ColumnInfo(
        "sample_size", "Samples", "Samples", "Number of samples", "n", False, False
    ),
    ColumnInfo("python", "Python", "Python", "Python version", "", False, False),
    #
    # --- Metric columns ---
    #
    # Properties that are unique for one single Benchmark instance.
    # The order of these columns is determines the default order in reports.
    #
    ColumnInfo("min", "min", "Minimum time", "Minimum time (best)", "s", True, False),
    ColumnInfo(
        "mean", "x̄", "Mean (x̄)", "Arithmetic mean ('average')", "s", True, False
    ),
    ColumnInfo("median", "Median", "Median", "Middle value", "s", True, False),
    ColumnInfo("q1", "Q1", "Q1", "First quartile", "s", True, False),
    ColumnInfo("iqr", "IQR", "IQR", "Interquartile Range, Q3 - Q1", "s", True, False),
    ColumnInfo("q3", "Q3", "Q3", "Third quartile", "s", True, False),
    ColumnInfo("max", "max", "Max. time", "Maximum time (worst)", "s", True, False),
    ColumnInfo("stdev", "σ", "Std Dev (σ)", "Standard deviation", "s", True, False),
    ColumnInfo("outliers", "Outliers", "", "", "n", True, False),
    ColumnInfo(
        "ops", "maxOPS", "maxOPS", "Maximum operations per second", "1/s", True, True
    ),
    ColumnInfo(
        "ops_rel",
        "OPSrel",
        "OPSrel",
        "Maximum OPS relative to sample_size",
        "1/s",
        True,
        True,
    ),
]

#: Map column id -> ColumnInfo
COL_INFO_MAP = {col.id: col for col in COL_INFO_LIST}

#: All known column ids
COL_ID_SET = set(COL_INFO_MAP.keys())

#: Properties that are known for every Benchmark instance.
#: However, the values can occur more than once in a benchmark suite.
#: These can be used as row headers or dynamic columns in a dataset.
DYNAMIC_COL_ID_SET = set(col.id for col in COL_INFO_LIST if col.metric is False)

#: Properties that are unique for one single Benchmark instance.
#: These can be used as static columns in a dataset.
METRIC_COL_ID_LIST = [col.id for col in COL_INFO_LIST if col.metric is True]

METRIC_COL_ID_SET = set(METRIC_COL_ID_LIST)


# def get_col_info(col: str) -> ColumnInfo:
#     """Lookup the information for a column id."""
#     return COL_INFO_MAP[col]


class DataCell:
    """A single cell in a dataset."""

    def __init__(
        self,
        attr: str,
        value: float | str | None,
        *,
        row: DataRow,
        col: str | None = None,
    ):
        self.attr = attr
        self.col = attr if col is None else col
        self.value = value
        self.row = row
        self.classes: set[str] = set()

    def __str__(self):
        return f"{self.attr}={self.value!r} ({','.join(self.classes)})"

    def __repr__(self):
        return f"{self.__class__.__name__}<{self}>"

    def __eq__(self, other):
        return self.value == other

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    @property
    def benchmark(self) -> Benchmark:
        return self.row.benchmark

    @property
    def col_info(self) -> ColumnInfo:
        return COL_INFO_MAP[self.attr]

    @property
    def dataset(self) -> Dataset:
        return self.row.dataset

    @property
    def is_dynamic(self) -> bool:
        return self.attr != self.col

    @property
    def is_metric(self) -> bool:
        return self.attr in METRIC_COL_ID_SET

    @property
    def is_fixed(self) -> bool:
        return not (self.is_dynamic or self.is_metric)


@dataclass(frozen=True)
class DataRow:
    """Single row of data in a dataset.

    Columns are represented by Benchmark instances, so we can easily
    access the values (e.v. `br.python`) and metrics (e.g. `br.min`).
    """

    dataset: Dataset
    benchmark: Benchmark
    cells: list[DataCell] = field(default_factory=list)
    classes: set[str] = field(default_factory=set)

    def __str__(self):
        return f"{self.cells}"

    def __repr__(self):
        return f"DataRow<{self.cells}>"

    def __iter__(self):
        yield from self.cells

    def __getitem__(self, key: int) -> DataCell:
        return self.cells[key]

    def __lt__(self, other):
        return self.cells < other.values

    def append_value(self, attr_name: str, value: float | str | None) -> DataCell:
        cell = DataCell(attr_name, value, row=self)
        self.cells.append(cell)
        return cell

    def float_values(self, *, param: str) -> list[float]:
        return [getattr(v, param) for v in self.cells]


class Dataset:
    """A class to represent a dataset of benchmarks structured by two parameters."""

    def __init__(
        self,
        *,
        name: str,
        bm: BenchmarkManager,
        cols: str | list[str],  # = ["full_name", "python", "best", "stdev"],
        dyn_col_name_attr: str | None = None,
        dyn_col_value_attr: str | None = None,
        filter: Callable[[Benchmark], bool] | str | None = None,
        sort_cols: Callable[[DataRow], Any] | str | None = None,
    ):
        self._initialized = False

        self.name: str = name
        self.bm = bm

        self.hardware = bm.loaded_context.get("hardware", bm.context.hw.slug())
        self.sysstem = bm.loaded_context.get("sysstem", bm.context.os.slug())

        if isinstance(cols, str):
            self.cols = [cols]
        else:
            self.cols = cols

        if self.cols == ["all"]:
            self.cols = [col.id for col in COL_INFO_LIST]
            self.cols.remove("full_name")

        col_id_set = set(self.cols)
        if not col_id_set.issubset(COL_ID_SET):
            raise ValueError(
                f"Invalid column(s) {col_id_set - COL_ID_SET}. "
                f"Expected one of {COL_ID_SET}"
            )

        self.dyn_col_name_attr = dyn_col_name_attr
        if dyn_col_name_attr and dyn_col_name_attr not in DYNAMIC_COL_ID_SET:
            raise ValueError(
                f"Invalid dyn_col_name_attr {dyn_col_name_attr!r}. "
                f"Expected one of {DYNAMIC_COL_ID_SET}"
            )
        self.dyn_col_value_attr = dyn_col_value_attr
        if dyn_col_value_attr and dyn_col_value_attr not in METRIC_COL_ID_SET:
            raise ValueError(
                f"Invalid dyn_col_value_attr {dyn_col_value_attr!r}. "
                f"Expected one of {METRIC_COL_ID_SET}"
            )

        # Headers are a combination of fixed columns and dynamic columns
        # (if any). We also expand the 'full_metrics' keyword to all metrics.
        header = []
        for col in self.cols.copy():
            if col == "full_metrics":
                header.extend(METRIC_COL_ID_LIST)
                self.cols.remove(col)
                self.cols.extend(METRIC_COL_ID_LIST)
            else:
                header.append(col)

        self.header_titles: list[str] = header

        self.rows: list[DataRow] = []
        self.col_to_index: dict[str, int] = {}

        self.original_count = bm.count()

        self.invisible_constant_dimensions: dict[str, Any] = {}
        self.ambigous_dimensions: set[str] = set()
        self.time_scale_by_benchmark_name: dict[str, tuple[TimeScale, TimeScale]] = {}

        if bool(dyn_col_name_attr) != bool(dyn_col_value_attr):
            raise ValueError(
                "col_name_attr and col_value_attr must be both set or None"
            )
        self.is_dynamic = bool(dyn_col_name_attr)

        # The filter can be a callable or a string that is parsed as an expression
        # (e.g. "python == '3.9' and best > 1000")
        self._filter_rule: str | None = None
        self.filter: Callable[[Benchmark], bool] | None = None
        if isinstance(filter, str):
            self._filter_rule = filter
            ef = ExpressionFilter(filter)
            self.filter = ef.matches
        elif callable(filter):
            self.filter = filter

        self._sort_col_attrs: list[str] | None = None

        self.sort_cols: Callable[[DataRow], Any] | None = None

        if sort_cols is None:
            self._sort_col_attrs = [self.cols[0]]
            self.sort_cols = self._sort_col_key

        if isinstance(sort_cols, str):
            self._sort_col_attrs = split_tokens(sort_cols)
            self.sort_cols = self._sort_col_key
        elif callable(sort_cols):
            self.sort = sort_cols

        self._aggregate()

        self._classify()

    def __str__(self):
        return f"Dataset<{self.name!r}, {self.header_titles}, n={len(self.rows)}>"

    def __repr__(self):
        return str(self)

    def _get_row_val(self, row: DataRow, col: str) -> str | float | None:
        """Return the value of a column for a given row."""
        return row[self.col_to_index[col]].value

    def _iter_row_values(
        self, row: DataRow
    ) -> Iterator[tuple[str, str | float | None]]:
        """Return al column values as (attr_name, value) pairs."""
        for col in self.cols:
            yield col, self._get_row_val(row, col)

    def _sort_col_key(self, row: DataRow) -> tuple[str | float | None, ...]:
        """Return a tuple of values that can be used to sort a row."""
        res = []
        assert self._sort_col_attrs
        for col in self._sort_col_attrs:
            reverse = False
            if col.startswith("-"):
                col = col[1:]
                reverse = True
            val = row[self.col_to_index[col]].value
            val = smart_sort_key(val)
            if reverse and isinstance(val, float):
                val = -val
            res.append(val)
        # print(f"{res=}   #   ", tuple(res))
        return tuple(res)

    def print(self):
        logger.info(self)
        # logger.info(self.header)
        for row in self.rows:
            logger.info(row)

    @classmethod
    def _classify_cell_list(cls, cells: list[DataCell], class_prefix: str) -> None:
        """Classify a list of DataCell objects into good/bad."""
        # print("classify", class_prefix, cells, "\n")
        cell_values: list[float] = [
            float(cell.value) for cell in cells if isinstance(cell.value, (int, float))
        ]
        if not cell_values:
            return  # need at leas one float value to classify

        q1, _q2, q3 = calculate_q1_q2_q3(cell_values)
        min_val = min(cell_values)
        max_val = max(cell_values)

        inverse = cells[0].col_info.inverse
        if inverse:
            best, good, bad, worst = "worst", "bad", "good", "best"
        else:
            best, good, bad, worst = "best", "good", "bad", "worst"

        for cell in cells:
            if not isinstance(cell.value, (int, float)):
                continue
            value = float(cell.value)
            if value == min_val:
                cell.classes.add(f"{class_prefix}-{best}")
            elif value < q1:
                cell.classes.add(f"{class_prefix}-{good}")

            if value == max_val:
                cell.classes.add(f"{class_prefix}-{worst}")
            elif value > q3:
                cell.classes.add(f"{class_prefix}-{bad}")
        # print("cells", inverse, cells)
        return

    def _classify(self) -> None:
        """Classify all cells in the dataset."""

        cells_by_name: dict[tuple[str, str], list[DataCell]] = defaultdict(list)
        cells_by_variant: dict[tuple[str, str, str], list[DataCell]] = defaultdict(list)

        for row in self.rows:
            dyn_row_cells: list[DataCell] = []
            for cell in row.cells:
                cbm = cell.benchmark

                if cell.is_metric:
                    cell.classes.add("metric")
                    cells_by_name[(cbm.name, cell.col)].append(cell)
                    cells_by_variant[(cbm.name, cbm.variant, cell.col)].append(cell)

                if cell.is_dynamic:
                    cell.classes.add("dynamic")
                    dyn_row_cells.append(cell)

                if cell.is_fixed:
                    cell.classes.add("fixed")

            self._classify_cell_list(dyn_row_cells, "row")
            self._classify_cell_list(dyn_row_cells, "row")

        for cells in cells_by_name.values():
            self._classify_cell_list(cells, "name")

        for cells in cells_by_variant.values():
            self._classify_cell_list(cells, "variant")

        # Determine best time scale for each benchmark
        min_values_by_name: dict[str, list[float]] = defaultdict(list)
        for row in self.rows:
            bm = row.benchmark
            min_val = bm.min
            min_values_by_name[bm.name].append(min_val)

        for bm_name, min_values in min_values_by_name.items():
            min_val = min(min_values)
            self.time_scale_by_benchmark_name[bm_name] = (
                get_time_unit(min_val),  # for unit [s]
                get_time_unit(min_val * 1e3),  # for unit [ops]
            )

        return

    def _aggregate(self) -> None:
        if self._initialized:
            raise ValueError("Dataset is already initialized")
        self._initialized = True

        bm = self.bm
        filter = self.filter
        is_dynamic = self.is_dynamic

        # --- Pass 1: Collect all possible values for dynamic column headers

        dyn_col_names: list[str] = []
        if is_dynamic:
            assert self.dyn_col_name_attr and self.dyn_col_value_attr
            for br in bm.iter_benchmarks():
                if filter and not filter(br):
                    continue
                col_name = getattr(br, self.dyn_col_name_attr)
                if col_name not in dyn_col_names:
                    dyn_col_names.append(col_name)
            dyn_col_names.sort(key=smart_sort_key)

        # --- Pass 2: Append fixed cells for all rows and collect dynamic cells

        row_dict: dict[tuple[str], DataRow] = {}
        dyn_col_dict: dict[tuple[str], dict[str, DataCell]] = defaultdict(dict)
        ambiguous_benchmarks: list[Benchmark] = []

        # Fixed colums may be dimensions and/or metrics. Only dimensions are
        # used to detect duplicate rows.
        unique_fixed_cols = {c for c in self.cols if c not in METRIC_COL_ID_LIST}

        filtered = total = dropped = 0

        for br in bm.iter_benchmarks():
            total += 1

            if filter and not filter(br):
                filtered += 1
                logger.debug(f"Skipping unmatched row: {br}")
                continue

            row_key = tuple([getattr(br, p) for p in unique_fixed_cols])
            # print(f"{row_key=}, {br=}")

            if row_key in row_dict and not is_dynamic:
                dropped += 1
                ambiguous_benchmarks.append(br)
                self.ambigous_dimensions.add(str(row_key))
                logger.warning(f"Skipping ambiguous row: {row_key}: {br}")
                continue

            data_row = DataRow(self, br)

            if is_dynamic:
                # Collect dynamic column cells in a dict, so we can append them
                # to the row later
                assert self.dyn_col_name_attr and self.dyn_col_value_attr

                dyn_col_name = getattr(br, self.dyn_col_name_attr)
                if dyn_col_name in dyn_col_dict[row_key]:
                    ambiguous_benchmarks.append(br)
                    self.ambigous_dimensions.add(f"{dyn_col_name}")
                    logger.warning(
                        f"Skipping ambiguous row: {row_key} + {dyn_col_name}: {br}"
                    )
                    continue
                dyn_col_value = getattr(br, self.dyn_col_value_attr)
                dyn_col_cell = DataCell(
                    self.dyn_col_value_attr,
                    dyn_col_value,
                    row=data_row,
                    col=dyn_col_name,
                )
                dyn_col_dict[row_key][dyn_col_name] = dyn_col_cell

            # Add fixed column cells to the row
            for col in self.cols:
                # print(f"{br=}, {col=}")
                data_row.append_value(col, getattr(br, col))

            row_dict[row_key] = data_row

        # --- Pass 3: Append dynamic column cells to the rows

        if is_dynamic:
            assert self.dyn_col_name_attr
            # Append dynamic column cells to the rows
            for row_key, dyn_cols in dyn_col_dict.items():
                data_row = row_dict[row_key]

                for dcn in dyn_col_names:
                    dc = dyn_cols.get(dcn)
                    if dc is None:
                        dc = DataCell(
                            self.dyn_col_name_attr, None, row=data_row, col=dcn
                        )
                    data_row.cells.append(dc)

        # --- Pass 4: Create Dataset instance

        self.all_cols = self.cols + dyn_col_names
        self.col_to_index = {c: i for i, c in enumerate(self.all_cols)}

        # Use 'Header title' from `col_info_list`
        self.header_titles = [
            COL_INFO_MAP[col].title if col in COL_INFO_MAP else col
            for col in self.all_cols
        ]

        # --- Pass 5: Create DataRow instances and sort them

        self.rows = list(row_dict.values())

        if self._sort_col_attrs and any(
            col.lstrip("-") not in self.col_to_index for col in self._sort_col_attrs
        ):
            raise ValueError(
                f"Invalid sort column(s): {self._sort_col_attrs}"
                f"Expected columns from {self.cols}"
            )
        self.rows.sort(key=self.sort_cols)

        # Check some statistics

        if filtered:
            logger.info(
                f"Skipped {filtered}/{total} benchmarks "
                f"(did not match filter {self._filter_rule!r})"
            )

        if ambiguous_benchmarks:
            logger.warning(f"Warning: Skipped {len(ambiguous_benchmarks)} benchmarks.")
            logger.warning(
                "This happens most likely when multiple benchmarks have different "
                "values for one dimension that is not displayed as a column."
            )
            logger.warning(
                "To resolve this, either add the dimension as fixed column or "
                "use a filter restict benchmarks to a single dimension value."
            )
            logger.warning(
                f"Skipped benchmarks: {pprint.pformat(ambiguous_benchmarks, indent=4)}"
            )

    def get_description_info(self) -> dict[str, str | TLegendLines]:
        """Return a description of the dataset."""
        # Find all dimension columns that are not displayed but have a constant
        # value
        attrs_with_multi_values = set()

        const_dim_vals = {}
        for row in self.rows:
            bmr = row.benchmark
            for col_name, value in bmr.loaded_state().items():
                if col_name not in const_dim_vals:
                    const_dim_vals[col_name] = value
                elif const_dim_vals[col_name] != value:
                    attrs_with_multi_values.add(col_name)

        for attr in attrs_with_multi_values:
            const_dim_vals.pop(attr)

        self.invisible_constant_dimensions = const_dim_vals

        #
        title = self.name
        if title is None:
            if self.is_dynamic:
                title = f"{self.dyn_col_value_attr} by {self.dyn_col_name_attr}"
                title = title.capitalize()
            else:
                title = "Benchmark Data"

        legend: TLegendLines = []
        warnings: TLegendLines = []
        subtitle: TLegendLines = []
        res: dict[str, str | TLegendLines] = {
            "title": f"{title}",
            "subtitle": subtitle,
            "legend": legend,
            "warnings": warnings,
        }

        subtitle.append(("Client", f"{self.hardware}, {self.sysstem}"))

        legend.append(("Benchmark date", f"{self.bm.combine_date}"))

        if const_dim_vals:
            vals = ", ".join(f"{k}={v!r}" for k, v in sorted(const_dim_vals.items()))
            legend.append(("Fixed dataset values", f"{vals}."))

        if attrs_with_multi_values:
            legend.append(
                (
                    "Variant dataset values",
                    f"{', '.join(sorted(attrs_with_multi_values))}.",
                )
            )

        if self._filter_rule and self.original_count != len(self.rows):
            legend.append(
                (
                    "",
                    f"Showing {len(self.rows)} of {self.original_count} rows, "
                    f"applied filter: {self._filter_rule!r}.",
                )
            )
        elif self.original_count != len(self.rows):
            legend.append(
                ("", f"Showing {len(self.rows)} of {self.original_count} rows.")
            )
        else:
            legend.append(f"Showing {len(self.rows)} rows.")

        if self._sort_col_attrs:
            legend.append(f"Sort order: {', '.join(self._sort_col_attrs)}.")

        if self.ambigous_dimensions:
            warnings.append(
                "WARNING: Skipped one or more rows with ambiguous column values: "
                "Results are probably inaccurate!\n"
                "    This happens most likely when multiple benchmarks have "
                "different values for one dimension that is not displayed as a "
                "column.\n"
                "    To resolve this, either add the dimension as column or "
                "use a filter to restrict benchmarks to a single dimension value."
            )

        return res
