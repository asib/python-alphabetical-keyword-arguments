import libcst as cst
import pytest

from python_alphabetical_keyword_arguments.transformer import (
    FunctionParametersTransformer,
)


def _result(code: str) -> str:
    transformer = FunctionParametersTransformer()
    source_tree = cst.parse_module(code)
    modified_tree = source_tree.visit(transformer)

    return modified_tree.code


@pytest.mark.parametrize(
    ("input_code", "output_code"),
    (
        pytest.param(
            """def f(): pass""",
            """def f(): pass""",
            id="no function parameters",
        ),
        pytest.param(
            """def f(x): pass""",
            """def f(x): pass""",
            id="single positional function parameter",
        ),
        pytest.param(
            """def f(x, *, y): pass""",
            """def f(x, *, y): pass""",
            id="single positional, single keyword-only function parameter",
        ),
    ),
)
def test_all(input_code: str, output_code: str):
    pass
