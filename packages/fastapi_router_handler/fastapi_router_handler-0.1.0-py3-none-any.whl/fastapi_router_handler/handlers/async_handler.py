import logging
from typing import Any, Callable, Coroutine, Optional

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from ..types.custom_types import HandlerCallable
from .base import BaseExceptionHandler


class AsyncExceptionHandler(BaseExceptionHandler):
    def _get_logger(self) -> Optional[logging.Logger]:
        logger = self.logger
        if logger is not None:
            return logger
        else:
            logger = logging.getLogger("fastapi")
            if logger is not None:
                return logger
        return None

    def _check_async_callable(
        self, func: HandlerCallable | dict | JSONResponse
    ) -> bool:
        return callable(func) and hasattr(func, "__await__")

    async def exception_handler(
        self,
        func: HandlerCallable | dict | JSONResponse,
        func_params: Optional[Any] = None,
        e_code: Optional[int] = None,
        e_msg: Optional[object] = None,
        additional_error_handle: Optional[Callable] = None,
    ) -> Any:
        try:
            if not callable(func):
                return func

            if self._check_async_callable(func):
                if func_params:
                    result = await func(func_params)
                else:
                    result = await func()
            else:
                if func_params:
                    result = func(func_params)
                else:
                    result = func()

            if isinstance(result, Coroutine):
                result = await result
            return result
        except Exception as e:
            return await self._handle_error(
                e=e,
                e_code=e_code,
                e_msg=e_msg,
                ae_handle=additional_error_handle,
            )

    async def _handle_error(
        self,
        e: Exception,
        e_code: Optional[int] = 500,
        e_msg: Optional[str] = "Internal Server Error",
        ae_handle: Optional[Callable] = None,
    ) -> Any:
        logger = self._get_logger()
        if logger:
            logger.error(f"Error occurred: {str(e)}")

        if ae_handle:
            try:
                if self._check_async_callable(ae_handle):
                    return await ae_handle(e)
                return ae_handle(e)
            except Exception as handler_error:
                if logger:
                    logger.error(
                        f"Error in custom handler: {str(handler_error)}",
                    )

        raise HTTPException(
            status_code=e_code or 500,
            detail=e_msg or str(e),
        )
