from typing import List

import msgspec
from stofory_sdk.catalog.models.enums import Locale, ProductKind, ProductType

__all__ = ('LanguagesInfoResponse', 'PlatformInfoResponse', 'CatalogFilterResponse')


class LanguagesInfoResponse(msgspec.Struct, forbid_unknown_fields=True):
    id: int
    language: Locale
    # is_enabled: bool


class PlatformInfoResponse(msgspec.Struct, forbid_unknown_fields=True):
    id: int
    name: str


class RegionInfo(msgspec.Struct, forbid_unknown_fields=True):
    id: int
    name_ru: str
    name_en: str
    alpha2: str


class OriginPlatformInfo(msgspec.Struct, forbid_unknown_fields=True):
    id: int
    name: str


class CatalogFilterResponse(msgspec.Struct, forbid_unknown_fields=True):
    regions: List[RegionInfo]
    origin_platforms: List[OriginPlatformInfo]
    product_types: List[ProductType]
    product_kinds: List[ProductKind]
