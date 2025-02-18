"""API client."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Generic, TypeVar

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pypco import PCO

from ._typing import get_return_type
from .base import App
from .services import Services
from .utils import singleton


class _Auth(BaseSettings):
    """Authentication."""

    model_config = SettingsConfigDict(env_file=".env")

    client_id: SecretStr
    client_secret: SecretStr


A = TypeVar("A", bound=App)


class app(property, Generic[A]):  # noqa: N801
    """Property that returns an instance of the annotated type."""

    def __init__(
        self,
        fget: Callable[[Client], A] | None = None,
        fset: Callable[[Client, Any], None] | None = None,
        fdel: Callable[[Client], None] | None = None,
        doc: str | None = None,
    ) -> None:
        """Initialize property."""
        super().__init__(fget, fset, fdel, doc)

    def __get__(self: app[A], instance: Client | None, owner: type[Client]) -> A:
        """Return the app type."""
        if instance:
            return_type: type[A] = get_return_type(self.fget)  # type: ignore[arg-type]
            return return_type(instance._pco)
        return super().__get__(instance, owner)


@singleton
class Client:
    """API client."""

    def __init__(self) -> None:
        """Initialize client."""
        auth = _Auth()
        self._pco = PCO(
            application_id=auth.client_id.get_secret_value(),
            secret=auth.client_secret.get_secret_value(),
        )

    @app
    def services(self) -> Services:
        """Services API wrapper."""
