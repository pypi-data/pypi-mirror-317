from datetime import datetime
from typing import Annotated

from litestar.params import Parameter
from msgspec import Struct


class OriginPlatformCreateRequest(Struct, forbid_unknown_fields=True):
    name: Annotated[
        str,
        Parameter(
            title="Название платформы",
            description="The name of the origin platform."
        )
    ]
    slug: Annotated[
        str,
        Parameter(
            title="Slug",
            description="A human-readable identifier for the platform."
        )
    ]


class OriginPlatformUpdateRequest(Struct, forbid_unknown_fields=True):
    name: Annotated[
        str,
        Parameter(
            title="Название платформы",
            description="Обновленное название платформы происхождения."
        )
    ]
    slug: Annotated[
        str,
        Parameter(
            title="Slug",
            description="Обновленный человекочитаемый идентификатор платформы."
        )
    ]


class OriginPlatformResponse(Struct):
    id: int
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime


class OriginPlatformShortResponse(Struct):
    id: int
    name: str
