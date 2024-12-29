from types import CoroutineType
from typing import Any, Callable, TypeVar, Union

T = TypeVar("T")
AsyncCallable = Callable[..., CoroutineType[Any, Any, T]]
SyncCallable = Callable[..., T]
HandlerCallable = Union[AsyncCallable, SyncCallable]
