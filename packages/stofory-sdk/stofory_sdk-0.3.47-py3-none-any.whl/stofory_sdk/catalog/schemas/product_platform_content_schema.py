from datetime import datetime
from typing import Annotated

from litestar.params import Parameter
from msgspec import Struct

from ..models.enums import ContentType


class ProductPlatformContentCreateRequest(Struct):
    product_platform_id: Annotated[int, Parameter(int, ge=1, title="Product Platform ID")]
    content_type: Annotated[ContentType, Parameter(ContentType, title="Content Type", description="The type of content.")]
    value: Annotated[str, Parameter(str, title="Content", description="The content of the product platform.")]


class ProductPlatformContentUpdateRequest(Struct):
    value: Annotated[str, Parameter(str, title="Content", description="The content of the product platform.")]


class ProductPlatformContentResponse(Struct):
    id: int
    product_platform_id: int
    content_type: ContentType
    value: str
    created_at: datetime
    updated_at: datetime
