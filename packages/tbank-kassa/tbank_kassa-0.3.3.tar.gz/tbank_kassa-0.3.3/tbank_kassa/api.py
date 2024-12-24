import hashlib
from typing import Any, Unpack

from .client import TBankKassaClient
from .enums import TBankKassaEnvironment
from .logger import logger
from .models import dicts, request, response


class TBankAPI:
    def __init__(
        self,
        terminal_key: str,
        password: str,
        environment: TBankKassaEnvironment = TBankKassaEnvironment.PROD,
    ):
        self._client = TBankKassaClient(
            environment=environment,
        )
        self._terminal_key = terminal_key
        self._password = password
        logger.info(
            'T-Bank API is ready now!'
                '\n\tTerminal "%s".'
                '\n\tEnvironment "%s".',
            self._terminal_key,
            environment.value,
        )

    def validate_webhook(self, data: dict[str, Any]) -> bool:
        token_dict = {}
        for key, value in {
            **data,
            'Password': self._password,
        }.items():
            if key == 'Token':
                continue
            if isinstance(value, dict):
                continue
            if isinstance(value, bool):
                value = str(value).lower()
            token_dict[key] = str(value)
        token = ''.join(token_dict[key] for key in sorted(token_dict))
        token = hashlib.sha256(token.encode('utf-8')).hexdigest()
        return token == data.get('Token')

    async def ainit_payment(self, **kwargs: Unpack[dicts.InitDict]):
        return await self._client.apost(
            request.Init(
                password=self._password,
                terminal_key=self._terminal_key,
                **kwargs,
            ),
            response.Payment,
        )

    def init_payment(self, **kwargs: Unpack[dicts.InitDict]):
        return self._client.post(
            request.Init(
                password=self._password,
                terminal_key=self._terminal_key,
                **kwargs,
            ),
            response.Payment,
        )
