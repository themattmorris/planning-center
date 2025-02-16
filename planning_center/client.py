"""API client."""

from __future__ import annotations

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


class app_property(property):  # noqa: N801
    """Property that returns an instance of the annotated type."""

    def __get__(self, instance: Client | None, owner: type[Client]) -> App:  # type: ignore[override]
        """Return the app type."""
        if instance:
            return_type: type[App] = get_return_type(self.fget)  # type: ignore[arg-type]
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

    @app_property
    def services(self) -> Services:
        """Services API wrapper."""
