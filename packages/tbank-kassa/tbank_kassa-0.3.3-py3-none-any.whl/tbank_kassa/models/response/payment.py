from pydantic import Field, HttpUrl

from .. import fields
from .response import Response


class Payment(Response):
    """
    Платеж
    """

    terminal_key: fields.TerminalKey = Field(
        validation_alias='TerminalKey',
    )
    """
    Идентификатор терминала.

    Выдается мерчанту Т‑Кассой при заведении терминала.
    """

    amount: fields.Amount = Field(
        validation_alias='Amount',
    )
    """
    Сумма платежа.
    """

    order_id: str = Field(
        validation_alias='OrderId',
        max_length=36,
    )
    """
    Идентификатор заказа в системе мерчанта.
    """

    status: str = Field(
        validation_alias='Status',
        max_length=20,
    )
    """
    Статус транзакции.
    """

    payment_id: str = Field(
        validation_alias='PaymentId',
        max_length=20,
    )
    """
    Идентификатор платежа в системе Т‑Кассы.
    """

    payment_url: HttpUrl | None = Field(
        validation_alias='PaymentURL',
        default=None,
    )
    """
    Ссылка на платежную форму.
    Параметр возвращается только для мерчантов без PCI DSS.
    """

