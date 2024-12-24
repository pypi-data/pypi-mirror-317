from decimal import Decimal
from typing import Annotated, Any

from pydantic import Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

TerminalKey = Annotated[
    str,
    Field(
        max_length=20,
    ),
]
"""
Идентификатор терминала.

Выдается мерчанту Т‑Кассой при заведении терминала.
"""


class Amount(Decimal):
    """
    Сумма платежа.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        base_schema = core_schema.decimal_schema(
            max_digits=10,
            decimal_places=2,
        )
        return core_schema.with_info_after_validator_function(
            function=lambda x, info: (
                x / Decimal('100')
                if (
                    isinstance(info.context, dict)
                    and info.context.get('tbank_kassa_format', False)
                )
                else x
            ),
            schema=base_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(
                function=lambda x, info: (
                    int(x * Decimal('100'))
                    if (
                        isinstance(info.context, dict)
                        and info.context.get('tbank_kassa_format', False)
                    )
                    else x
                ),
                info_arg=True,
                return_schema=core_schema.union_schema([
                    base_schema,
                    core_schema.int_schema(),
                ]),
                when_used='unless-none',
            ),
        )
