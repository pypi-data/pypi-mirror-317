from datetime import datetime
from typing import Annotated, Optional

from litestar.params import Parameter
from msgspec import Struct

from stofory_sdk.catalog.models.enums import ProductType, ProductKind

from .product_platform_schema import ProductPlatformResponse


class ProductCreateRequest(Struct, forbid_unknown_fields=True):
    name: Annotated[
        str,
        Parameter(
            title="Name",
            description="The name of the product."
        )
    ]
    description: Annotated[
        str,
        Parameter(
            title="Description",
            description="The description of the product."
        )
    ]
    product_type: Annotated[
        ProductType,
        Parameter(
            title="Product Type",
            description="The type of the product."
        )
    ]
    product_kind: Annotated[
        ProductKind,
        Parameter(
            title="Product Kind",
            description="The kind of the product."
        )
    ]
    slug: Annotated[
        str,
        Parameter(
            title="Slug",
            description="The slug of the product."
        )
    ]
    origin_platform_id: Annotated[
        int,
        Parameter(
            title="Origin Platform ID",
            description="The ID of the origin platform."
        )
    ]
    region_buy_id: Annotated[
        int,
        Parameter(
            title="Region Buy ID",
            description="The ID of the region where the product is bought."
        )
    ]
    regions_sale_ids: Annotated[
        Optional[list[int]],
        Parameter(
            title="Regions Sale IDs",
            description="The list of IDs of regions where the product is sold."
        )
    ]


class ProductUpdateRequest(Struct, forbid_unknown_fields=True):
    name: Annotated[
        Optional[str],
        Parameter(
            title="Name",
            description="The name of the product."
        )
    ]
    description: Annotated[
        Optional[str],
        Parameter(
            title="Description",
            description="The description of the product."
        )
    ]
    product_type: Annotated[
        Optional[ProductType],
        Parameter(
            title="Product Type",
            description="The type of the product."
        )
    ]
    product_kind: Annotated[
        Optional[ProductKind],
        Parameter(
            title="Product Kind",
            description="The kind of the product."
        )
    ]
    status: Annotated[
        Optional[bool],
        Parameter(
            title="Status",
            description="The status of the product. True for active, False for inactive."
        )
    ]
    slug: Annotated[
        Optional[str],
        Parameter(
            title="Slug",
            description="The slug of the product."
        )
    ]
    origin_platform_id: Annotated[
        Optional[int],
        Parameter(
            title="Origin Platform ID",
            description="The ID of the origin platform."
        )
    ]
    region_buy_id: Annotated[
        Optional[int],
        Parameter(
            title="Region Buy ID",
            description="The ID of the region where the product is bought."
        )
    ]
    regions_sale_ids: Annotated[
        Optional[list[int]],
        Parameter(
            title="Regions Sale IDs",
            description="The list of IDs of regions where the product is sold."
        )
    ]


class ProductResponse(Struct):
    id: int
    name: str
    description: str
    product_type: ProductType
    product_kind: ProductKind
    status: bool
    slug: str
    origin_platform_id: int
    region_buy_id: int
    regions_sale_ids: Optional[list[int]]
    created_at: datetime
    updated_at: datetime

    product_platforms: list[ProductPlatformResponse]


class PlatformShortResponse(Struct):
    id: int
    name: str


class ProductPlatformShortWithPlatformResponse(Struct):
    id: int
    platform: PlatformShortResponse


class ProductShortenedResponse(ProductResponse):
    product_platforms: list[ProductPlatformShortWithPlatformResponse]
