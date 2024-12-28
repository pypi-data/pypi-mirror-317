# (c) 2024 Martin Wendt; see https://github.com/mar10/benchman
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php

import datetime
import json
import platform
import pprint
import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any

from benchman import BenchmarkManager
from benchman.benchman import get_benchmark_filepath
from benchman.dataset import Dataset
from benchman.reporter import TablibReporter
from benchman.util import (
    BenchmarkSuiteFile,
    extract_items,
    json_dump,
    logger,
    split_tokens,
)


def handle_combine_command(parser: ArgumentParser, args: Namespace) -> int:
    bm = BenchmarkManager.singleton()
    data: list[dict[str, Any]] = []
    combined: dict[str, Any] = {
        "combine_date": datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
        "context": None,
        "data": data,
    }
    #: The keys that must be common to all benchmark files
    common_context_keys = [
        "client",
        "debug_mode",
        "hardware",
        "project",
        "version",
        "system",
        "tag",
    ]
    combined_files: list[Path] = []
    first_context: dict[str, Any] | None = None
    errors = 0

    for p in bm.folder.glob("*.bmr.json"):
        with p.open("r") as f:
            benchmark_data = json.load(f)

        # Extract specific items from the dictionary
        common_context = extract_items(benchmark_data, common_context_keys, remove=True)

        if first_context is None:
            first_context = common_context
            combined["context"] = common_context
            combined["tag"] = bm.tag
        else:
            # Check if the context is the same
            mismatch = []
            for k, v in common_context.items():
                if v != first_context.get(k):
                    mismatch.append((k, v, first_context.get(k)))
                    continue
            if mismatch:
                errors += 1
                logger.warning(
                    "Found benchmark with different context information:\n"
                    "  " + pprint.pformat(mismatch) + "\n"
                    "  Skipping file: " + str(p)
                )
                continue

        # We now have read a benchmark file that has the same context as the
        # first one.
        data.append(benchmark_data)
        combined_files.append(p)

    if len(data) < 1:
        logger.warning(f"No benchmark files found in {bm.folder}")
        return 2

    target_path = get_benchmark_filepath(args.tag)
    with target_path.open("w") as f:
        json_dump(combined, f, pretty=True)

    if not args.no_purge and not errors:
        for p in combined_files:
            logger.debug(f"Delete {p}")
            p.unlink()

    logger.info(f"Combined {len(data)} benchmark files into {target_path}")
    return 3 if errors else 0


def handle_info_command(parser: ArgumentParser, args: Namespace):
    bm = BenchmarkManager.singleton()
    uname = platform.uname()

    files = BenchmarkSuiteFile.find_files(bm.folder)
    tags = sorted(list({f.tag for f in files}))

    logger.info("Benchman (https://github.com/mar10/benchman):")
    logger.info(f"  Project   : {bm.project_name} v{bm.project_version}")
    logger.info(f"  Folder    : {bm.folder}")
    logger.info(f"  Node      : {uname.node}")
    logger.info(f"  System    : {uname.system} {uname.release}")
    logger.info(f"  Machine   : {uname.machine}")
    logger.info(f"  Client ID : {bm.context.client_slug()}")
    logger.info(f'  Tags      : {", ".join(tags)}')

    if args.list:
        logger.info(f"{len(files)} benchmark suites:")
        for f in files:
            logger.info(f"  {f.name}")
    return


def handle_run_command(parser: ArgumentParser, args: Namespace):
    raise NotImplementedError("Not implemented yet.")


def handle_purge_command(parser: ArgumentParser, args: Namespace):
    bm = BenchmarkManager.singleton()
    orphans = list(bm.folder.glob("*.bmr.json"))
    for p in orphans:
        logger.debug(f"Delete {p}")
        p.unlink()
    logger.info(f"Deleted {len(orphans)} uncombined temporary benchmark files.")


def handle_report_command(parser: ArgumentParser, args: Namespace):
    path = get_benchmark_filepath(args.input)
    bm = BenchmarkManager.load(path)

    ds = Dataset(
        name=args.name,
        bm=bm,
        cols=split_tokens(args.columns),
        dyn_col_name_attr=args.dyn_col_name,
        dyn_col_value_attr=args.dyn_col_value,
        filter=args.filter,
        sort_cols=args.sort,
    )

    r = TablibReporter(ds)
    r.report(format=args.format, out=args.output)


def handle_tag_command(parser: ArgumentParser, args: Namespace):
    source_path = get_benchmark_filepath(args.source, must_exist=True)
    target_path = get_benchmark_filepath(args.name, must_exist=False)

    if target_path.exists() and not args.force:
        logger.error(f"Target file already exists: {target_path}")
        logger.info("Hint: pass --force to overwrite.")
        return 1

    bm_file = BenchmarkSuiteFile(source_path)
    bm_file.save_tag(args.name, replace=False, keep_time=args.keep_time)

    if args.git_add:
        logger.info(f"git add {target_path}")

        result = subprocess.run(
            ["git", "add", "-v", "-f", target_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode != 0:
            logger.error(f"Error running `git add -f`: {result.stdout.decode()}")
            return 1
        logger.info(f"File '{target_path}' added to git index.")
    return
