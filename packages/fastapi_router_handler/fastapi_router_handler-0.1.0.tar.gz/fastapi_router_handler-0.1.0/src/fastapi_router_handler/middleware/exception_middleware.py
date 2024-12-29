from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from ..handlers.base import BaseExceptionHandler


class ExceptionMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        exception_handler: BaseExceptionHandler,
    ) -> None:
        super().__init__(app)
        self.exception_handler = exception_handler

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return self.exception_handler.handle_exception(exc)
