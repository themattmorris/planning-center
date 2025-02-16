"""Generic utilities."""

from __future__ import annotations

from typing import Any, Generic, cast

from ._typing import C, T


class _SingletonWrapper(Generic[T]):
    """A singleton wrapper class. Its instances would be created for each decorated
    class. This was taken from `singleton-decorator` library.
    """

    def __init__(self, cls: type[T]) -> None:
        self.__wrapped__ = cls
        self._instance: T | None = None

    def __getattr__(self, __name: str) -> Any:
        return getattr(self.__wrapped__, __name)

    def __call__(self: _SingletonWrapper[T], *args: Any, **kwargs: Any) -> T:
        """Returns a single instance of decorated class."""
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)
        return self._instance


def singleton(cls: C) -> C:
    """A singleton decorator. Returns a wrapper object. A call on that object returns a
    single instance object of decorated class. Use the __wrapped__ attribute to access
    decorated class directly in unit tests.
    """
    result = _SingletonWrapper(cls)
    result.__name__ = cls.__name__  # type: ignore[attr-defined]
    result.__doc__ = cls.__doc__
    return cast(C, result)
