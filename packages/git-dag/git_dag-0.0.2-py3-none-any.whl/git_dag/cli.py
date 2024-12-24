#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""Comman-line interface."""
import argparse
import logging

import argcomplete

from .git_repository import GitRepository


def get_cla_parser() -> argparse.ArgumentParser:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Visualize the git DAG.")

    parser.add_argument(
        "-p",
        "--path",
        default=".",
        help="Path to git repository.",
    )

    parser.add_argument(
        "-f",
        "--file",
        default="git-dag.gv",
        help="Output graphviz file (could include a directory e.g., mydir/myfile).",
    )

    parser.add_argument(
        "--format",
        default="svg",
        help=(
            "Graphviz output format (tooltips are available only with svg). "
            "If the format is set to 'gv', only the graphviz source file is generated"
        ),
    )

    parser.add_argument(
        "--dpi",
        help="DPI of output figure (normally used with --format png).",
    )

    parser.add_argument(
        "-i",
        "--init-refs",
        nargs="+",
        help=(
            "A list of SHA of object (commits, tags, trees, blobs) that represents "
            "a limitation from where to display the DAG"
        ),
    )

    parser.add_argument(
        "-n",
        "--max-numb-commits",
        type=int,
        default=1000,  # default protection
        help="Max number of commits.",
    )

    parser.add_argument(
        "--rankdir",
        help="rankdir argument of graphviz (LR, RL, TB, BT).",
    )

    parser.add_argument(
        "--bgcolor",
        default="gray42",
        help="bgcolor argument of graphviz (e.g., transparent).",
    )

    parser.add_argument(
        "-t",
        dest="show_tags",
        action="store_true",
        help="Show tags.",
    )

    parser.add_argument(
        "-l",
        dest="show_local_branches",
        action="store_true",
        help="Show local branches.",
    )

    parser.add_argument(
        "-r",
        dest="show_remote_branches",
        action="store_true",
        help="Show remote branches.",
    )

    parser.add_argument(
        "-s",
        dest="show_stash",
        action="store_true",
        help="Show stash.",
    )

    parser.add_argument(
        "-T",
        dest="show_trees",
        action="store_true",
        help="Show trees (WARNING: should be used only with small repositories).",
    )

    parser.add_argument(
        "-B",
        dest="show_blobs",
        action="store_true",
        help="Show blobs (discarded if -T is not set).",
    )

    parser.add_argument(
        "-o",
        "--xdg-open",
        action="store_true",
        help="Open output SVG file with xdg-open.",
    )

    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["NOTSET", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Log level.",
    )

    return parser


def main() -> None:
    """CLI entry poit."""
    parser = get_cla_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    logging.getLogger().setLevel(getattr(logging, args.log_level))

    GitRepository(args.path, parse_trees=args.show_trees).show(
        xdg_open=args.xdg_open,
        format=args.format,
        show_tags=args.show_tags,
        show_local_branches=args.show_local_branches,
        show_remote_branches=args.show_remote_branches,
        show_trees=args.show_trees,
        show_blobs=args.show_blobs,
        show_stash=args.show_stash,
        starting_objects=args.init_refs,
        filename=args.file,
        graph_attr={
            "rankdir": args.rankdir,
            "dpi": args.dpi,
            "bgcolor": args.bgcolor,
        },
        max_numb_commits=args.max_numb_commits,
    )


if __name__ == "__main__":
    main()
