import argparse
import pathlib
import sys

from . import cli

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="python_alphabetical_keyword_arguments",
        description="Sort keyword-only function parameters alphabetically",
    )
    parser.add_argument(
        "path",
        metavar="PATH",
        type=pathlib.Path,
        nargs="+",
    )
    parser.add_argument(
        "--check",
        action="store_true",
    )

    args = parser.parse_args()

    would_rewrite = False
    for path in args.path:
        would_rewrite |= cli.run(path=path, check=args.check)

    sys.exit(1 if would_rewrite else 0)
