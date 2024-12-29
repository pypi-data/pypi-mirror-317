import logging
from typing import Optional

from .handlers.async_handler import AsyncExceptionHandler
from .middleware.exception_middleware import ExceptionMiddleware


class ExceptionHandler(AsyncExceptionHandler):
    def __init__(self, logger: Optional[logging.Logger] = None):
        super().__init__(logger)


__all__ = ["ExceptionHandler", "ExceptionMiddleware"]
