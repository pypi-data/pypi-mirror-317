from datetime import datetime
from typing import Annotated, Any

from sqlalchemy_utils.types.ltree import Ltree
from litestar.params import Parameter
from msgspec import Struct

from .category_name_schema import CategoryNameResponse


class CategoryCreateRequest(Struct, forbid_unknown_fields=True):
    platform_id: Annotated[
        int,
        Parameter(
            title="Platform ID",
            description="The ID of the platform."
        )
    ]
    path: Annotated[
        Any,
        Parameter(
            title="Path",
            description="The path of the category."
        )
    ]
    parent_id: Annotated[
        int | None,
        Parameter(
            title="Parent ID",
            description="The ID of the parent category."
        )
    ] = None
    external_id: Annotated[
        int | None,
        Parameter(
            title="External ID",
            description="The external ID of the category."
        )
    ] = None
    external_parent_id: Annotated[
        int | None,
        Parameter(
            title="External Parent ID",
            description="The external ID of the parent category."
        )
    ] = None
    is_owner: Annotated[
        bool,
        Parameter(
            title="Is Owner",
            description="The owner flag of the category."
        )
    ] = False
    is_subcategory: Annotated[
        bool,
        Parameter(
            title="Is Subcategory",
            description="The subcategory flag of the category."
        )
    ] = False


class CategoryUpdateRequest(Struct, forbid_unknown_fields=True):
    platform_id: Annotated[
        int,
        Parameter(
            title="Platform ID",
            description="The ID of the platform."
        )
    ]
    parent_id: Annotated[
        int | None,
        Parameter(
            title="Parent ID",
            description="The ID of the parent category."
        )
    ]
    path: Annotated[
        Any,
        Parameter(
            title="Path",
            description="The path of the category."
        )
    ]
    external_id: Annotated[
        int | None,
        Parameter(
            title="External ID",
            description="The external ID of the category."
        )
    ] = None
    external_parent_id: Annotated[
        int | None,
        Parameter(
            title="External Parent ID",
            description="The external ID of the parent category."
        )
    ] = None
    is_owner: Annotated[
        bool,
        Parameter(
            title="Is Owner",
            description="The owner flag of the category."
        )
    ] = False
    is_subcategory: Annotated[
        bool,
        Parameter(
            title="Is Subcategory",
            description="The subcategory flag of the category."
        )
    ] = False


class CategoryResponse(Struct):
    id: int
    platform_id: int
    parent_id: int | None
    path: Any
    external_id: int | None
    external_parent_id: int | None
    is_owner: bool
    is_subcategory: bool
    created_at: datetime
    updated_at: datetime

    names: list[CategoryNameResponse]

    children_count: int | None = None
