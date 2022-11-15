from abc import ABC
from http import HTTPStatus
from typing import Type

from fastapi import Request
from fastapi.responses import JSONResponse


class MessengerServiceException(Exception, ABC):
    code: HTTPStatus
    message: str


class InvalidCodeException(MessengerServiceException):
    code = HTTPStatus.UNAUTHORIZED
    message = "Code is invalid"


async def messenger_exception_handler(_: Request, exc: Type[MessengerServiceException]) -> JSONResponse:
    return JSONResponse(status_code=exc.code.value, content={"detail": exc.message})
