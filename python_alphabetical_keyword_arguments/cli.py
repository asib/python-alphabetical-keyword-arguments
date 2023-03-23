import os
import pathlib

import libcst as cst

from python_alphabetical_keyword_arguments.transformer import (
    FunctionParametersTransformer,
)


def run(
    *,
    check: bool,
    path: pathlib.Path,
) -> bool:
    if path.is_file():
        return _run_file(path=path, check=check)
    elif path.is_dir():
        return _run_directory(path=path, check=check)
    else:
        raise Exception("unknown path type")


def _run_file(
    *,
    check: bool,
    path: pathlib.Path,
) -> bool:
    code = path.read_text()
    transformer = FunctionParametersTransformer()

    source_tree = cst.parse_module(code)
    modified_tree = source_tree.visit(transformer)

    if not check:
        path.write_text(modified_tree.code)

    return code != modified_tree.code


def _run_directory(
    *,
    check: bool,
    path: pathlib.Path,
) -> bool:
    did_rewrite = False

    for directory_path, _, file_names in os.walk(path):
        did_rewrite |= any(
            _run_file(
                path=pathlib.Path(directory_path, file_name),
                check=check,
            )
            for file_name in file_names
            if file_name.endswith(".py")
        )

    return did_rewrite
