from typing import NotRequired, TypedDict

from ..request.init import (
    HttpUrl,
    ReceiptFFD12,
    ReceiptFFD105,
    Shop,
    datetime,
    enums,
    fields,
)


class InitDict(TypedDict):
    amount: fields.Amount
    order_id: str
    description: NotRequired[str]
    customer_key: NotRequired[str]
    recurrent: NotRequired[str]
    payment_type: NotRequired[enums.PaymentType]
    language: NotRequired[enums.Language]
    notification_url: NotRequired[HttpUrl]
    success_url: NotRequired[HttpUrl]
    fail_url: NotRequired[HttpUrl]
    time_to_live: NotRequired[datetime]
    extra: NotRequired[dict]
    receipt: NotRequired[ReceiptFFD105 | ReceiptFFD12]
    shops: NotRequired[list[Shop]]
    descriptor: NotRequired[str]
