from datetime import datetime
from typing import Annotated, Any

from litestar.params import Parameter
from msgspec import Struct

from . import (
    # ProductPlatformCreateRequest,     # base struct for create request schemas?

    ProductPlatformNameCreateRequest,
    ProductPlatformDescriptionCreateRequest,
    ProductPlatformCategoryCreateRequest,
    ProductPlatformPricingCreateRequest,
    ProductPlatformBonusCreateRequest,
    ProductPlatformDiscountCreateRequest,
    ProductPlatformGuaranteeCreateRequest,
    ProductPlatformNameUpdateRequest,
    ProductPlatformDescriptionUpdateRequest,
    ProductPlatformCategoryUpdateRequest,
    ProductPlatformPricingUpdateRequest,
    ProductPlatformBonusUpdateRequest,
    ProductPlatformDiscountUpdateRequest,
    ProductPlatformGuaranteeUpdateRequest,
    ProductPlatformImageCreateRequest,
    ProductPlatformImageUpdateRequest,
    ProductPlatformVideoCreateRequest,
    ProductPlatformVideoUpdateRequest,
    ProductPlatformParameterCreateRequest,
    ParameterNameCreateRequest,
    ParameterCommentCreateRequest,
    ParameterOptionCreateRequest,
    ParameterOptionNameCreateRequest,
    ProductPlatformParameterUpdateRequest,
    ParameterNameUpdateRequest,
    ParameterCommentUpdateRequest,
    ParameterOptionUpdateRequest,
    ParameterOptionNameUpdateRequest, CategoryCreateRequest, CategoryUpdateRequest,
)
from .category_name_schema import CategoryNameCreateRequest, CategoryNameUpdateRequest


# Wrapper for all isolated update request schemas
class GenericUpdateRequest[T, U](Struct, forbid_unknown_fields=True):
    id: int | None = None
    update: T | None = None
    create: U | None = None

    def __post_init__(self):
        if self.update is not None and self.create is not None:
            raise ValueError("Only one of 'update' or 'create' should be specified")

        if self.update is None and self.create is None:
            raise ValueError("One of 'update' or 'create' should be specified")

        if self.update is not None and self.id is None:
            raise ValueError("Id should be specified for 'update'")

        if self.create is not None and self.id is not None:
            raise ValueError("Id should not be specified for 'create'")


# Basic group
class BasicGroupCreateRequest(Struct, forbid_unknown_fields=True):
    names: list[ProductPlatformNameCreateRequest]
    descriptions: list[ProductPlatformDescriptionCreateRequest]
    categories: list[ProductPlatformCategoryCreateRequest]
    price: ProductPlatformPricingCreateRequest
    bonus: ProductPlatformBonusCreateRequest | None
    discount: ProductPlatformDiscountCreateRequest | None
    guarantee: ProductPlatformGuaranteeCreateRequest | None


class BasicGroupUpdateRequest(Struct, forbid_unknown_fields=True):
    is_visible: bool
    names: list[GenericUpdateRequest[ProductPlatformNameUpdateRequest, ProductPlatformNameCreateRequest]]
    descriptions: list[GenericUpdateRequest[ProductPlatformDescriptionUpdateRequest, ProductPlatformDescriptionCreateRequest]]
    categories: list[GenericUpdateRequest[ProductPlatformCategoryUpdateRequest, ProductPlatformCategoryCreateRequest]]
    price: GenericUpdateRequest[ProductPlatformPricingUpdateRequest, ProductPlatformPricingCreateRequest]
    bonus: GenericUpdateRequest[ProductPlatformBonusUpdateRequest, ProductPlatformBonusCreateRequest] | None
    discount: GenericUpdateRequest[ProductPlatformDiscountUpdateRequest, ProductPlatformDiscountCreateRequest] | None
    guarantee: GenericUpdateRequest[ProductPlatformGuaranteeUpdateRequest, ProductPlatformGuaranteeCreateRequest] | None


# Gallery group
class GalleryGroupCreateRequest(Struct, forbid_unknown_fields=True):
    images: list[ProductPlatformImageCreateRequest]
    videos: list[ProductPlatformVideoCreateRequest]


class GalleryGroupUpdateRequest(Struct, forbid_unknown_fields=True):
    images: list[GenericUpdateRequest[ProductPlatformImageUpdateRequest, ProductPlatformImageCreateRequest]]
    videos: list[GenericUpdateRequest[ProductPlatformVideoUpdateRequest, ProductPlatformVideoCreateRequest]]


# Parameters group
class GroupParameterOptionCreateRequest(ParameterOptionCreateRequest, forbid_unknown_fields=True):
    names: list[GenericUpdateRequest[None, ParameterOptionNameCreateRequest]]


class GroupParameterCreateRequest(ProductPlatformParameterCreateRequest, forbid_unknown_fields=True):
    names: list[GenericUpdateRequest[None, ParameterNameCreateRequest]]
    comments: list[GenericUpdateRequest[None, ParameterCommentCreateRequest]]
    options: list[GenericUpdateRequest[None, GroupParameterOptionCreateRequest]]


class ParametersGroupCreateRequest(Struct, forbid_unknown_fields=True):
    parameters: list[GenericUpdateRequest[None, GroupParameterCreateRequest]]


class GroupParameterOptionUpdateRequest(ParameterOptionUpdateRequest, forbid_unknown_fields=True):
    names: list[GenericUpdateRequest[ParameterOptionNameUpdateRequest, ParameterOptionNameCreateRequest]]


class GroupParameterUpdateRequest(ProductPlatformParameterUpdateRequest, forbid_unknown_fields=True):
    names: list[GenericUpdateRequest[ParameterNameUpdateRequest, ParameterNameCreateRequest]]
    comments: list[GenericUpdateRequest[ParameterCommentUpdateRequest, ParameterCommentCreateRequest]]
    options: list[GenericUpdateRequest[GroupParameterOptionUpdateRequest, GroupParameterOptionCreateRequest]]


class ParametersGroupUpdateRequest(Struct, forbid_unknown_fields=True):
    parameters: list[GenericUpdateRequest[GroupParameterUpdateRequest, GroupParameterCreateRequest]]


class CategoryGroupCreateRequest(CategoryCreateRequest, forbid_unknown_fields=True, kw_only=True):
    names: list[CategoryNameCreateRequest]


class CategoryGroupUpdateRequest(CategoryUpdateRequest, forbid_unknown_fields=True, kw_only=True):
    names: list[GenericUpdateRequest[CategoryNameUpdateRequest, CategoryNameCreateRequest]]
