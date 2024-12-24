from typing import TypeVar

import requests
from aiohttp import ClientSession
from pydantic import ValidationError

from . import enums
from .logger import logger
from .models.request.request import Request
from .models.response.response import Response

RESPONSE = TypeVar('RESPONSE', bound=Response)


class TBankKassaClient:
    def __init__(
        self,
        environment: enums.TBankKassaEnvironment,
    ):
        match environment:
            case enums.TBankKassaEnvironment.TEST:
                self._base_url = 'https://rest-api-test.tinkoff.ru/v2'
            case enums.TBankKassaEnvironment.PROD:
                self._base_url = 'https://securepay.tinkoff.ru/v2'
            case _:
                raise AttributeError()

    def _bytes_to_response(
        self,
        data: bytes,
        response_model: type[RESPONSE],
    ) -> Response | RESPONSE:
        try:
            response = Response.prepare(data)
        except ValidationError:
            logger.exception('Cannot validate response.')
            raise
        if not response.success:
            logger.warning(
                'Response is unsuccessful. '
                    '(code: "%s", message: "%s", details: "%s")',
                response.error_code,
                response.error_message,
                response.error_details,
            )
            return response
        return response_model.prepare(data)

    async def apost(
        self,
        request: Request,
        response_model: type[RESPONSE],
    ) -> Response | RESPONSE:
        async with (
            ClientSession() as session,
            session.post(
                url=request.get_url(self._base_url),
                json=request.prepare(),
            ) as response,
        ):
            logger.info('(async) POST %d "%s"', response.status, response.url)
            return self._bytes_to_response(
                await response.read(),
                response_model,
            )

    def post(
        self,
        request: Request,
        response_model: type[RESPONSE],
    ) -> Response | RESPONSE:
        response = requests.post(
            url=request.get_url(self._base_url),
            json=request.prepare(),
            timeout=10,
        )
        logger.info('POST %d "%s"', response.status_code, response.url)
        return self._bytes_to_response(
            response.content,
            response_model,
        )
