from typing import Optional, List
from stofory_sdk.catalog.models.enums import ProductType, ProductKind, Currency, ParameterType, ModifierOperator, \
    PricingType
import msgspec

__all__ = ('CatalogProductsRequest', 'CatalogProductsRegion', 'CatalogProductsResponse', 'ProductInfoResponse')

from stofory_sdk.lib.schemas.filters_and_sorting_schema import SortingRulesSchema, SortType


class CatalogProductsRequest(SortingRulesSchema, forbid_unknown_fields=True):
    """
    Модель запроса для получения списка товаров из каталога с фильтрацией и пагинацией.
    """
    platform_id: int  # Идентификатор платформы для отображения товаров
    lang_id: int  # Идентификатор языка для отображения информации о товарах
    currency: Currency  # Идентификатор валюты для отображения информации о товарах

    origin_platform_product: Optional[int] = None  # Идентификатор платформы товара для фильтрации
    type_product: Optional[ProductType] = None  # Тип товара для фильтрации (например, 'physical', 'digital')
    kind_product: Optional[ProductKind] = None  # Категория товара для фильтрации (например, 'key', 'account')
    region_sell: Optional[int] = None  # Регион продажи товара для фильтрации (например, 'RU', 'US')

    price_min: Optional[float] = None  # Минимальная цена товара для фильтрации (включительно)
    price_max: Optional[float] = None  # Максимальная цена товара для фильтрации (включительно)

    is_discount: Optional[bool] = None  # Фильтр по наличию скидки (True - со скидкой, False - без скидки)
    is_enabled: Optional[bool] = None  # Фильтр по наличию на складе (True - в наличии, False - нет в наличии)

    page: int = 1  # Номер страницы для пагинации (начиная с 1)
    page_size: int = 10  # Количество товаров на странице (минимум 10, максимум 100)

    search_string: Optional[str] = None  # Значение для поиска

    s__name: Optional[SortType] = None
    s__price: Optional[SortType] = None
    s__platform: Optional[SortType] = None
    s__product_type: Optional[SortType] = None
    s__product_kind: Optional[SortType] = None
    s__region: Optional[SortType] = None


class CatalogProductsRegion(msgspec.Struct):
    id: int
    alpha2: str


class InfoPricing(msgspec.Struct):
    id: int
    pricing_type: PricingType
    price: int | None
    price_per_unit: int | None
    min_quantity: int | None
    max_quantity: int | None
    unit_name: str | None
    currency: Currency


class CatalogProductsResponse(msgspec.Struct, kw_only=True):
    id: int
    lang_id: int
    name: str
    image_domain: str
    image_relative_path: str
    pricing: InfoPricing
    currency: Currency
    is_enabled_discount: bool
    discount: float
    platform: str
    product_type: ProductType
    product_kind: ProductKind
    region_info: List[CatalogProductsRegion]


class InfoImage(msgspec.Struct):
    id: int
    domain: str
    relative_path: str


class InfoParameterOption(msgspec.Struct):
    id: int
    name: str
    order: int
    is_default: bool
    is_enabled: bool
    modifier_operator: ModifierOperator
    modifier_value: int


class InfoParameter(msgspec.Struct):
    id: int
    name: str
    comment: str
    order: int
    is_required: bool
    parameter_type: ParameterType
    options: List[InfoParameterOption]


class ProductInfoResponse(msgspec.Struct, kw_only=True):
    id: int
    name: str
    platform: str
    description: str
    discount: int
    pricing: InfoPricing
    images: List[InfoImage]
    region_info: List[CatalogProductsRegion]
    parameters: List[InfoParameter]
