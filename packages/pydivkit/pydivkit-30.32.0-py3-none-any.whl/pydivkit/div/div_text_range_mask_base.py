# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field


class DivTextRangeMaskBase(BaseDiv):

    def __init__(
        self, *,
        is_enabled: typing.Optional[typing.Union[Expr, bool]] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            is_enabled=is_enabled,
            **kwargs,
        )

    is_enabled: typing.Optional[typing.Union[Expr, bool]] = Field(
        description=(
            "Controls mask state: if set to `true` mask will hide "
            "specified part of the text,otherwise the text will be "
            "shown."
        ),
    )


DivTextRangeMaskBase.update_forward_refs()
