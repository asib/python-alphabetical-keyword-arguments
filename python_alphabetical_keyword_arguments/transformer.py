from typing import Union

import libcst as cst


class FunctionParametersTransformer(cst.CSTTransformer):
    def leave_FunctionDef(
        self,
        original_node: cst.FunctionDef,
        updated_node: cst.FunctionDef,
    ) -> Union[
        cst.BaseStatement,
        cst.FlattenSentinel[cst.BaseStatement],
        cst.RemovalSentinel,
    ]:
        sorted_keyword_parameters = sorted(
            original_node.params.kwonly_params,
            key=lambda param: param.name.value,
        )

        sorted_keyword_parameters = [
            param.with_changes(
                comma=cst.Comma(
                    whitespace_after=cst.SimpleWhitespace(" "),
                    whitespace_before=cst.SimpleWhitespace(""),
                )
            )
            for param in sorted_keyword_parameters
        ]

        return updated_node.with_changes(
            params=original_node.params.with_changes(
                kwonly_params=sorted_keyword_parameters
            )
        )
