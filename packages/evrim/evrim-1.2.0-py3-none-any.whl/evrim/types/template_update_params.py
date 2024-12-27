# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["TemplateUpdateParams", "Field"]


class TemplateUpdateParams(TypedDict, total=False):
    description: Optional[str]

    fields: Iterable[Field]

    name: str

    questions: List[str]


class Field(TypedDict, total=False):
    description: Required[str]

    name: Required[str]

    type: Required[str]

    id: int

    enum_many: bool

    enum_values: List[str]

    rel_template: Optional[int]

    rel_template_id: Optional[int]
