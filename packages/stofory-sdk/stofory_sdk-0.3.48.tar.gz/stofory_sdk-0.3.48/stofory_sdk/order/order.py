import enum
from typing import Optional

import msgspec


class NewOrderRequest(msgspec.Struct, forbid_unknown_fields=True):
    product_id: str
    platform: Optional[str] = None


class TypeOrder(enum.StrEnum):
    Undefined = 'Undefined'
    Steam_Gift = 'Steam_Gift'
    Steam_Balance_Refill = 'Steam_Balance_Refill'


class MinimalPaymentResponse(msgspec.Struct, forbid_unknown_fields=True):
    id_goods: int
    amount: float
    type_curr: str
    date_pay: str
    email: str
    unit_goods: Optional[int] = None
    cnt_goods: Optional[float] = None
    name: str = None
    type: TypeOrder = None


class OrderInfoResponse(msgspec.Struct, forbid_unknown_fields=True):
    data: Optional[MinimalPaymentResponse]


class OrderStatusResponse(msgspec.Struct, forbid_unknown_fields=True):
    status: Optional[str]
