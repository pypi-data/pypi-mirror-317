# (c) 2024 Martin Wendt; see https://github.com/mar10/benchman
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
"""
Usage examples:
    $ benchman --help
    $ benchman freeze
"""
# ruff: noqa: T201, T203 `print` found

import argparse
import logging
import os
import platform
import sys
from typing import Any

from snazzy import Snazzy, enable_colors

from benchman.benchman import TAG_BASE, TAG_LATEST
from benchman.cli_commands import (
    handle_combine_command,
    handle_info_command,
    handle_purge_command,
    handle_report_command,
    handle_run_command,
    handle_tag_command,
)
from benchman.util import PYTHON_VERSION, get_project_info, logger

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    # format="%(asctime)-8s.%(msecs)-3d <%(thread)05d> %(levelname)-7s %(message)s",
    datefmt="%H:%M:%S",
)
# If basicConfig() was already called before, the above call was a no-op.
# Make sure, we adjust the level still:
# logging.root.setLevel(level)


__version__ = get_project_info().get("version", "0.0.0")

# --- verbose_parser ----------------------------------------------------------

verbose_parser = argparse.ArgumentParser(
    add_help=False,
    # allow_abbrev=False,
)

qv_group = verbose_parser.add_mutually_exclusive_group()
qv_group.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=3,
    help="increment verbosity by one (default: %(default)s, range: 0..5)",
)
qv_group.add_argument(
    "-q", "--quiet", default=0, action="count", help="decrement verbosity by one"
)

# --- common_parser ----------------------------------------------------------

common_parser = argparse.ArgumentParser(
    add_help=False,
    # allow_abbrev=False,
)
# common_parser.add_argument(
#     "-n",
#     "--dry-run",
#     action="store_true",
#     help="just simulate and log results, but don't change anything",
# )
common_parser.add_argument(
    "--no-color", action="store_true", help="prevent use of ansi terminal color codes"
)


# ===============================================================================
# run
# ===============================================================================
def run() -> Any:
    """CLI main entry point."""

    parents = [verbose_parser, common_parser]

    parser = argparse.ArgumentParser(
        description="Collect and analyze microbenchmarks.",
        epilog="See also https://github.com/mar10/benchman",
        parents=parents,
        allow_abbrev=False,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="display version info and exit (combine with -v for more information)",
    )
    subparsers = parser.add_subparsers(help="sub-command help")

    # --- Create the parser for the "combine" command -----------------------------

    sp = subparsers.add_parser(
        "combine",
        parents=parents,
        allow_abbrev=False,
        help="combine latest benchmark results into a single file",
    )
    sp.add_argument(
        "--tag",
        default="latest",
        help="only combine benchmark files with this tag (default: %(default)s)",
    )
    sp.add_argument(
        "--no-purge",
        action="store_true",
        help="keep single benchmark files after combining",
    )
    sp.add_argument(
        "--force",
        action="store_true",
        help="overwrite existing combined file if any",
    )
    sp.set_defaults(cmd_handler=handle_combine_command, cmd_name="combine")

    # --- Create the parser for the "info" command -----------------------------

    sp = subparsers.add_parser(
        "info",
        parents=parents,
        allow_abbrev=False,
        help="dump information about the available benchmark results",
    )
    sp.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="list all benchmark files",
    )
    sp.set_defaults(cmd_handler=handle_info_command, cmd_name="info")

    # --- Create the parser for the "purge" command ----------------------------

    sp = subparsers.add_parser(
        "purge",
        parents=parents,
        allow_abbrev=False,
        help="remove latest uncombined benchmark results",
    )
    sp.set_defaults(cmd_handler=handle_purge_command, cmd_name="purge")

    # --- Create the parser for the "report" command ---------------------------

    sp = subparsers.add_parser(
        "report",
        parents=parents,
        allow_abbrev=False,
        help="create a report from benchmark results",
    )
    sp.add_argument(
        "--input",
        default="latest",
        help="input file name, path, or tag (default: %(default)s)",
    )
    sp.add_argument(
        "--name",
        help="report title",
    )
    sp.add_argument(
        "--columns",
        # default="full_name,version,python,best,ops,ops_rel,stdev",
        default="full_name,python,min,ops,ops_rel,stdev",
        help="comma separated list of columns to keep in the report "
        "(default: %(default)s)",
    )
    sp.add_argument(
        "--dyn-col-name",
        help=(
            "benchmark dimension to create different columns for "
            "(e.g. 'sample_size','project', 'python', ...)"
        ),
    )
    sp.add_argument(
        "--dyn-col-value",
        # default="ops",
        help=(
            "benchmark attribute to use as value for dynamic column rows "
            "(e.g. 'best', 'ops', 'mean', ...)"
        ),
    )
    sp.add_argument(
        "--filter",
        help=(
            "filter rows by expression, e.g. "
            "'--filter \"python ^= 3.12, fullname *= bubble\"'"
        ),
    )
    sp.add_argument(
        "--sort",
        help=(
            "comma separated list of columns to sort by. "
            "Prefix with '-' for descending (e.g. 'full_name,python,-ops')"
        ),
    )
    sp.add_argument(
        "--format",
        # see https://tablib.readthedocs.io/en/stable/formats.html
        choices=["html", "markdown", "csv", "json", "yaml", "df"],
        default="markdown",
        help="report output format (default: %(default)s)",
    )
    sp.add_argument(
        "--output",
        help="output file name (default: stdout)",
    )
    sp.add_argument(
        "--append",
        action="store_true",
        help="append to existing file (overwrite otherwise)",
    )
    sp.add_argument(
        "--open",
        action="store_true",
        help="open file in browser after successful run",
    )

    sp.set_defaults(cmd_handler=handle_report_command, cmd_name="report")

    # --- Create the parser for the "run" command ------------------------------

    sp = subparsers.add_parser(
        "run",
        parents=parents,
        allow_abbrev=False,
        help="run and benchmark terminal applications",
    )
    sp.set_defaults(cmd_handler=handle_run_command, cmd_name="run")

    # --- Create the parser for the "tag" command ------------------------------

    sp = subparsers.add_parser(
        "tag",
        parents=parents,
        allow_abbrev=False,
        help="Copy existing benchmark results to make it persistent",
    )
    sp.add_argument(
        "--source",
        default=TAG_LATEST,
        help=(
            "tag name of an existing file that will be copied "
            "(default: '%(default)s')"
        ),
    )
    sp.add_argument(
        "-n",
        "--name",
        default=TAG_BASE,
        help="new tag name (default: '%(default)s')",
    )
    sp.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite existing tag file if any",
    )
    sp.add_argument(
        "--keep-time",
        action="store_true",
        help="keep the original timestamp of the source file",
    )
    sp.add_argument(
        "--git-add",
        action="store_true",
        help="run `git add -f` after successful tagging",
    )
    sp.set_defaults(cmd_handler=handle_tag_command, cmd_name="tag")

    # --- Parse command line ---------------------------------------------------

    args = parser.parse_args()

    args.verbose -= args.quiet
    del args.quiet  # type: ignore

    # print("verbose", args.verbose)
    # init_logging(args.verbose)  # , args.log_file)
    if args.verbose >= 4:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if not args.no_color:
        # Enable terminal colors (if sys.stdout.isatty())
        enable_colors(True, force=False)
        if os.environ.get("TERM_PROGRAM") == "vscode":
            Snazzy._support_emoji = True  # VSCode can do

    if getattr(args, "version", None):
        if args.verbose >= 4:
            version_info = "benchman/{} {}/{}({} bit) {}".format(
                __version__,
                platform.python_implementation(),
                PYTHON_VERSION,
                "64" if sys.maxsize > 2**32 else "32",
                platform.platform(aliased=False),
            )
            version_info += f"\nPython from: {sys.executable}"
        else:
            version_info = __version__
        print(version_info)
        sys.exit(0)

    if not callable(getattr(args, "cmd_handler", None)):
        parser.error("missing command")

    try:
        return args.cmd_handler(parser, args)
    # except click.ClickException as e:
    #     print(f"{e!r}", file=sys.stderr)
    #     sys.exit(2)
    # except (KeyboardInterrupt, click.Abort):
    except KeyboardInterrupt:
        print("\nAborted by user.", file=sys.stderr)
        sys.exit(3)
    # Unreachable...


# Script entry point
if __name__ == "__main__":
    # Just in case...
    from multiprocessing import freeze_support

    freeze_support()

    run()
