import pathlib
import tempfile
from typing import List

import pytest
from precisely import assert_that, equal_to

from python_alphabetical_keyword_arguments.cli import run


@pytest.fixture(name="file")
def _fixture_file(tmp_path: pathlib.Path):
    file_path = tmp_path / "tmp.py"
    file_path.touch()
    return file_path


@pytest.fixture(name="directory")
def _fixture_directory(tmp_path: pathlib.Path):
    directory_path = tmp_path / "tmp_dir"
    directory_path.mkdir()
    return directory_path


@pytest.mark.parametrize(
    ("input_contents", "output_contents"),
    (
        pytest.param(
            """def f(): pass""",
            """def f(): pass""",
            id="rewrite case",
        ),
        pytest.param(
            """def f(*, y, x): pass""",
            """def f(*, x, y, ): pass""",
            id="rewrite case",
        ),
        pytest.param(
            """def f(*, x, y): pass""",
            """def f(*, x, y): pass""",
            id="rewrite case",
        ),
    ),
)
def test_file_rewrite(
    *,
    file: pathlib.Path,
    input_contents: str,
    output_contents: str,
) -> None:
    file.write_text(input_contents)

    rewrite_was_not_trivial = run(path=file, check=False)

    assert_that(file.read_text(), equal_to(output_contents))
    assert_that(
        rewrite_was_not_trivial,
        equal_to(input_contents != output_contents),
    )


@pytest.mark.parametrize(
    ("input_contents", "output_contents"),
    (
        pytest.param(
            ["""def f(): pass""", """def f(*, y, x): pass"""],
            ["""def f(): pass""", """def f(*, x, y, ): pass"""],
            id="rewrite multiple files in directory",
        ),
    ),
)
def test_directory_rewrite(
    *,
    directory: pathlib.Path,
    input_contents: List[str],
    output_contents: List[str],
) -> None:
    file_paths: List[pathlib.Path] = []
    for input_code in input_contents:
        file = tempfile.NamedTemporaryFile(
            dir=directory,
            mode="w",
            suffix=".py",
            delete=False,
        )
        file.write(input_code)
        file.flush()
        file_paths.append(directory / file.name)

    rewrite_was_not_trivial = run(path=directory, check=False)

    for file_path, output_code in zip(file_paths, output_contents):
        assert_that(file_path.read_text(), equal_to(output_code))

    assert_that(
        rewrite_was_not_trivial,
        equal_to(
            any(
                [
                    input_code != output_code
                    for (input_code, output_code) in zip(
                        input_contents, output_contents
                    )
                ]
            )
        ),
    )


def test_file_check_does_not_write_file(file: pathlib.Path) -> None:
    input_code = """def f(*, y, x): pass"""
    file.write_text(input_code)

    would_rewrite = run(path=file, check=True)

    assert_that(file.read_text(), equal_to(input_code))
    assert_that(would_rewrite, equal_to(True))


def test_directory_check_does_not_write_files(directory: pathlib.Path) -> None:
    input_a = """def f(): pass"""
    input_b = """def f(*, y, x): pass"""
    file_a = directory / "a.py"
    file_b = directory / "b.py"
    file_a.write_text(input_a)
    file_b.write_text(input_b)

    would_rewrite = run(path=directory, check=True)

    assert_that(file_a.read_text(), equal_to(input_a))
    assert_that(file_b.read_text(), equal_to(input_b))
    assert_that(would_rewrite, equal_to(True))
