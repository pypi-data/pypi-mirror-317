import logging
from typing import Any, Callable, Dict, Type

from fastapi import HTTPException


class BaseExceptionHandler:
    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger
        self.exception_handlers: Dict[Type[Exception], Callable] = {}

    def register_exception_handler(
        self,
        exception_class: Type[Exception],
        handler: Callable[[Exception], Any],
    ) -> None:
        self.exception_handlers[exception_class] = handler

    def handle_exception(self, exc: Exception) -> Any:
        for exc_class, handler in self.exception_handlers.items():
            if isinstance(exc, exc_class):
                return handler(exc)
        return HTTPException(status_code=500, detail=str(exc))
