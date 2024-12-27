from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import ParamSpec, Generic, Self, TypeIs, TypeAlias
import asyncio

from ki2_python_utils import CallbackList, AsyncCallbackList, run_parallel
from ki2_python_utils import CallbackType, AsyncCallbackType

if TYPE_CHECKING:
    from ki2_python_utils.list_utils import AsyncCallbackMode

_P = ParamSpec("_P")

DualContextCallbackType: TypeAlias = CallbackType[_P] | AsyncCallbackType[_P]


def _is_async_callback(
    callback: DualContextCallbackType[_P],
) -> TypeIs[AsyncCallbackType[_P]]:
    """
    Determines if the given callback is asynchronous.

    Args:
        callback (DualContextCallbackType[_P]): The callback to check.

    Returns:
        TypeIs[AsyncCallbackType[_P]]: True if the callback is asynchronous, False
        otherwise.
    """
    return asyncio.iscoroutinefunction(callback)


def _is_sync_callback(
    callback: DualContextCallbackType[_P],
) -> TypeIs[CallbackType[_P]]:
    """
    Determines if the given callback is synchronous.

    Args:
        callback (DualContextCallbackType[_P]): The callback to check.

    Returns:
        TypeIs[CallbackType[_P]]: True if the callback is synchronous, False otherwise.
    """
    return not _is_async_callback(callback)


class DualContextCallback(Generic[_P]):
    """
    A class for managing both synchronous and asynchronous callbacks.

    This class allows the registration and execution of both synchronous and
    asynchronous callbacks, providing a unified interface for managing them.
    """

    __sync: CallbackList[_P]
    __async: AsyncCallbackList[_P]

    def __init__(self) -> None:
        """
        Initializes the DualContextCallback instance.

        Creates separate lists for synchronous and asynchronous callbacks.
        """
        super().__init__()
        self.__sync = CallbackList()
        self.__async = AsyncCallbackList()

    def set_async_mode(self, mode: AsyncCallbackMode) -> Self:
        """
        Sets the default asynchronous call mode.

        Args:
            mode (AsyncCallbackMode): The mode to set for asynchronous callbacks.

        Returns:
            Self: The instance of the class for method chaining.
        """
        self.__async.default_call_mode = mode
        return self

    def add_sync(self, callback: CallbackType[_P]) -> Self:
        """
        Adds a synchronous callback to the callback list.

        Args:
            callback (CallbackType[_P]): The synchronous callback to add.

        Returns:
            Self: The instance of the class for method chaining.
        """
        self.__sync.append(callback)
        return self

    def add_async(self, callback: AsyncCallbackType[_P]) -> Self:
        """
        Adds an asynchronous callback to the callback list.

        Args:
            callback (AsyncCallbackType[_P]): The asynchronous callback to add.

        Returns:
            Self: The instance of the class for method chaining.
        """
        self.__async.append(callback)
        return self

    def add(self, callback: DualContextCallbackType[_P]) -> Self:
        """
        Adds a callback, determining whether it is synchronous or asynchronous.

        Args:
            callback (DualContextCallbackType[_P]): The callback to add.

        Returns:
            Self: The instance of the class for method chaining.
        """
        if _is_async_callback(callback):
            self.add_async(callback)
        elif _is_sync_callback(callback):  # Only used to pass static analysis
            self.add_sync(callback)
        return self

    async def call_async(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        """
        Calls all registered callbacks asynchronously.

        This method supports both synchronous and asynchronous callbacks,
        executing them in the appropriate context.

        Args:
            *args: Positional arguments to pass to the callbacks.
            **kwargs: Keyword arguments to pass to the callbacks.
        """

        async def run_sync():
            await asyncio.to_thread(self.__sync.call, *args, **kwargs)

        async def run_async():
            await self.__async.call(*args, **kwargs)

        if self.__async.default_call_mode == "parallel":
            await run_parallel(run_sync, run_async)
        else:
            await run_sync()
            await run_async()

    def call_sync(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        """
        Calls all registered callbacks synchronously.

        This method includes asynchronous callbacks, running them in a blocking context.

        Args:
            *args: Positional arguments to pass to the callbacks.
            **kwargs: Keyword arguments to pass to the callbacks.
        """

        self.__sync.call(*args, **kwargs)
        asyncio.run(self.__async.call(*args, **kwargs))
