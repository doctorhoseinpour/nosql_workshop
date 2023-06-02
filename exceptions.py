from fastapi import Request
from starlette import status
from fastapi import FastAPI
from fastapi.responses import JSONResponse


class BaseMessage:
    def __init__(self, code, message, status_code):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.response = JSONResponse({
            'message': self.message,
            'error_code': self.code
        }, status_code=self.status_code)


class MongoDBException(Exception):
    def __init__(self, message: str):
        self.message = message

    status_code = status.HTTP_400_BAD_REQUEST
    error_code = 10


def handlers(app: FastAPI) -> None:
    @app.exception_handler(MongoDBException)
    async def unidentical_passwords_handler(request: Request, exc: MongoDBException):
        return BaseMessage(exc.error_code, exc.message, exc.status_code).response
