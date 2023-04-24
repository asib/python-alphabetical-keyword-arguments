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
    print_changes: bool,
) -> bool:
    if path.is_file():
        return _run_file(
            path=path,
            check=check,
            print_changes=print_changes,
        )
    elif path.is_dir():
        return _run_directory(
            path=path,
            check=check,
            print_changes=print_changes,
        )
    else:
        raise Exception("unknown path type")


def _run_file(
    *,
    check: bool,
    path: pathlib.Path,
    print_changes: bool,
) -> bool:
    code = path.read_text()
    transformer = FunctionParametersTransformer()

    source_tree = cst.parse_module(code)
    modified_tree = source_tree.visit(transformer)

    if not check:
        path.write_text(modified_tree.code)

    if print_changes and code != modified_tree.code:
        print(f"// -- {path.name} --:\n{modified_tree.code}")

    return code != modified_tree.code


def _run_directory(
    *,
    check: bool,
    path: pathlib.Path,
    print_changes: bool,
) -> bool:
    did_rewrite = False

    for directory_path, _, file_names in os.walk(path):
        did_rewrite |= any(
            _run_file(
                path=pathlib.Path(directory_path, file_name),
                check=check,
                print_changes=print_changes,
            )
            for file_name in file_names
            if file_name.endswith(".py")
        )

    return did_rewrite
