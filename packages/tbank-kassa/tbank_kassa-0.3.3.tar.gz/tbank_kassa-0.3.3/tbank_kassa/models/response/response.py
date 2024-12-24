from pydantic import BaseModel, Field


class Response(BaseModel):
    success: bool = Field(
        validation_alias='Success',
    )
    """
    Успешность прохождения запроса.
    """

    error_code: str = Field(
        validation_alias='ErrorCode',
        max_length=20,
    )
    """
    Код ошибки. 0 в случае успеха.
    """

    error_message: str | None = Field(
        validation_alias='Message',
        max_length=255,
        default=None,
    )
    """
    Краткое описание ошибки.
    """

    error_details: str | None = Field(
        validation_alias='Details',
        default=None,
    )
    """
    Подробное описание ошибки.
    """

    @classmethod
    def prepare(cls, data: bytes):
        return cls.model_validate_json(
            data,
            context={
                'tbank_kassa_format': True,
            },
        )
