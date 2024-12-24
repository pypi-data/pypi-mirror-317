import hashlib
from typing import Any

from pydantic import BaseModel, Field, PrivateAttr, HttpUrl


class Request(BaseModel):
    _method: str = PrivateAttr(
        default=None,
    )

    def get_url(self, base_url: HttpUrl) -> str:
        return f'{base_url}/{self.method}'

    @property
    def method(self) -> str:
        return self._method

    def prepare(self) -> dict[str, Any]:
        return self.model_dump(
            mode='json',
            by_alias=True,
            exclude_unset=True,
            context={
                'tbank_kassa_format': True,
            },
        )


class TokenRequest(Request):
    password: str = Field(
        max_length=20,
        serialization_alias='Password',
        exclude=True,
    )
    """
    Используется для подписи запросов/ответов. Является секретной информацией,
    известной только мерчанту и Т‑Кассе.

    Пароль находится в личном кабинете мерчанта.
    """

    token: str | None = Field(
        default=None,
        serialization_alias='Token',
        init=False,
    )

    def model_post_init(self, __context):
        token_dict = {}
        for key, value in {
            **self.model_dump(
                mode='json',
                by_alias=True,
                exclude={'token'},
                exclude_unset=True,
                context = {
                    'tbank_kassa_format': True,
                },
            ),
            'Password': self.password,
        }.items():
            if isinstance(value, dict):
                continue
            if isinstance(value, bool):
                value = str(value).lower()
            token_dict[key] = str(value)
        token = ''.join(token_dict[key] for key in sorted(token_dict))
        self.token = hashlib.sha256(token.encode('utf-8')).hexdigest()
