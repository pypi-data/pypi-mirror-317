from functools import lru_cache
from typing import Any, Callable, TypeVar, cast

T = TypeVar("T")


def cached_property(func: Callable[..., T]) -> property:
    """Implement a decorator similar to @property but with caching capabilities."""
    return property(lru_cache()(func))
