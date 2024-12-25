import inspect
from typing import Any, Awaitable, Callable, Coroutine
from typing_extensions import TypeIs

type AnyFunction[**P_AnyFunction, T_AnyFunction] = Callable[P_AnyFunction, T_AnyFunction] | Callable[
    P_AnyFunction, Coroutine[Any, Any, T_AnyFunction]
] | Callable[P_AnyFunction, Awaitable[T_AnyFunction]]
"""Any function type, synchronous or asynchronous. Can be used to type hint a function that can be either synchronous or asynchronous. """

type AsyncFunction[**P_AsyncFunction, T_AsyncFunction] = Callable[P_AsyncFunction, Coroutine[Any, Any, T_AsyncFunction]] | Callable[
    P_AsyncFunction, Awaitable[T_AsyncFunction]
]
"""Async function type. Can be used to type hint an asynchronous function."""


def is_async_function[
    T, **P
](func: AnyFunction[P, T]) -> TypeIs[AsyncFunction[P, T]]:
    return inspect.iscoroutinefunction(func)
