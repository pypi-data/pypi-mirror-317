from datetime import datetime
from typing import Annotated, Optional

from litestar.params import Parameter
from msgspec import Struct

from stofory_sdk.catalog.models.enums import LocationType, PartOfWorldType


class RegionCreateRequest(Struct, forbid_unknown_fields=True):
    name_ru: Annotated[
        str,
        Parameter(
            title="Название на русском",
            description="Название региона на русском языке.",
        )
    ]
    name_en: Annotated[
        str,
        Parameter(
            title="Название на английском",
            description="Название региона на английском языке.",
        )
    ]
    alpha2: Annotated[
        str,
        Parameter(
            title="Alpha2",
            description="Код региона в формате Alpha2 (2 символа).",
            pattern="^[A-Z]{2}$"
        )
    ]
    alpha3: Annotated[
        str,
        Parameter(
            title="Alpha3",
            description="Код региона в формате Alpha3 (3 символа).",
            pattern="^[A-Z]{3}$"
        )
    ]
    iso: Annotated[
        int,
        Parameter(
            title="ISO",
            description="ISO-код региона (числовой код).",
        )
    ]
    part_of_world: Annotated[
        PartOfWorldType | None,
        Parameter(
            title="Часть света",
            description="Часть света, к которой относится регион.",
        )
    ]
    location: Annotated[
        LocationType | None,
        Parameter(
            title="Расположение",
            description="Географическое расположение региона.",
        )
    ]


class RegionUpdateRequest(Struct, forbid_unknown_fields=True):
    name_ru: Annotated[
        Optional[str],
        Parameter(
            title="Название на русском",
            description="Название региона на русском языке.",
        )
    ]
    name_en: Annotated[
        Optional[str],
        Parameter(
            title="Название на английском",
            description="Название региона на английском языке.",
        )
    ]
    iso: Annotated[
        Optional[int],
        Parameter(
            title="ISO",
            description="ISO-код региона (числовой код).",
        )
    ]
    part_of_world: Annotated[
        Optional[PartOfWorldType],
        Parameter(
            title="Часть света",
            description="Часть света, к которой относится регион.",
        )
    ]
    location: Annotated[
        Optional[LocationType],
        Parameter(
            title="Расположение",
            description="Географическое расположение региона.",
        )
    ]


class RegionResponse(Struct):
    id: int
    name_ru: str
    name_en: str
    alpha2: str
    alpha3: str
    iso: int
    part_of_world: PartOfWorldType | None
    location: LocationType | None
    created_at: datetime
    updated_at: datetime


class RegionShortResponse(Struct):
    id: int
    name_ru: str
    name_en: str
    alpha2: str
    alpha3: str
