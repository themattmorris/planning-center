"""Type hinting."""

from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar, get_type_hints


C = TypeVar("C", bound=type[Any])
P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


def get_return_type(func: Callable[P, R]) -> type[R]:
    """Get the return type of a function."""
    return get_type_hints(func)["return"]
