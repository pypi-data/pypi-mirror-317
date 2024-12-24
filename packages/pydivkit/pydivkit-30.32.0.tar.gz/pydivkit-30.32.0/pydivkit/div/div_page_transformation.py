# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing
from typing import Union

from pydivkit.core import BaseDiv, Expr, Field

from . import div_page_transformation_overlap, div_page_transformation_slide


DivPageTransformation = Union[
    div_page_transformation_slide.DivPageTransformationSlide,
    div_page_transformation_overlap.DivPageTransformationOverlap,
]
