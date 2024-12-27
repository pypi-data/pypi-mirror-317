import enum
from typing import List

import msgspec

from stofory_sdk.digiseller.schemas import BaseResponse


class ContentFileNode(msgspec.Struct, forbid_unknown_fields=True):
    content_id: int
    filename: str


class AddTextNode(msgspec.Struct, forbid_unknown_fields=True):
    value: str
    id_v: int
    serial: str | None = None


class ContentTextNode(msgspec.Struct, forbid_unknown_fields=True):
    content_id: int
    serial: str | None = None


class ContentCode(msgspec.Struct, forbid_unknown_fields=True):
    status: str


class ContentFileEditNode(msgspec.Struct, forbid_unknown_fields=True):
    # content_id: int   # в доках есть, по факту нет
    new_content_id: int
    filename: str


class ContentDeleteAll(msgspec.Struct, forbid_unknown_fields=True):
    deleted_count: int


class DeliveryTypes(enum.StrEnum):
    Email = "Email"
    JSON = "JSON"
    XML = "XML"


class ContentForm(msgspec.Struct, forbid_unknown_fields=True):
    status: str


"""
    Request/Response schemas for N7
"""


class AddTextRequest(msgspec.Struct, forbid_unknown_fields=True):
    product_id: int
    content: list[AddTextNode]


class EditTextRequest(msgspec.Struct, forbid_unknown_fields=True):
    content_id: int
    value: str
    serial: str | None = None
    update_old: bool = False


class CreateEditFormRequest(msgspec.Struct, forbid_unknown_fields=True):
    product_id: int
    address: str
    method: DeliveryTypes
    encoding: str
    options: bool
    answer: bool
    allow_purchase_multiple_items: bool
    url: str | None = None


class AddFileResponse(BaseResponse, forbid_unknown_fields=True):
    content: List[ContentFileNode] | None


class AddTextResponse(BaseResponse, forbid_unknown_fields=True):
    content: List[ContentTextNode] | None


class UpdateCodeResponse(BaseResponse, forbid_unknown_fields=True):
    content: ContentCode | None


class UpdateFileResponse(BaseResponse, forbid_unknown_fields=True):
    content: ContentFileEditNode | None


class UpdateTextResponse(BaseResponse, forbid_unknown_fields=True):
    content: ContentTextNode | None


class DeleteContentResponse(BaseResponse, forbid_unknown_fields=True):
    content: ContentDeleteAll | None


class CreateEditFormResponse(BaseResponse, forbid_unknown_fields=True):
    content: ContentForm | None