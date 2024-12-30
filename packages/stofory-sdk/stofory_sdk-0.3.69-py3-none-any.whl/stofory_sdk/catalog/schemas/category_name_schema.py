from datetime import datetime
from typing import Annotated

from litestar.params import Parameter
from msgspec import Struct

from .localization_schema import LocalizationResponse


class CategoryNameCreateRequest(Struct, forbid_unknown_fields=True):
    category_id: Annotated[int, Parameter(title="Category ID", description="The ID of the category.")]
    localization_id: Annotated[
        int,
        Parameter(
            title="Localization ID",
            description="The ID of the localization."
        )
    ]
    value: Annotated[
        str,
        Parameter(
            title="Value",
            description="The value of the category name."
        )
    ]


class CategoryNameUpdateRequest(Struct, forbid_unknown_fields=True):
    value: Annotated[
        str,
        Parameter(
            title="Value",
            description="The value of the category name."
        )
    ]


class CategoryNameResponse(Struct):
    id: int
    category_id: int
    localization_id: int
    value: str
    created_at: datetime
    updated_at: datetime

    locale: LocalizationResponse
