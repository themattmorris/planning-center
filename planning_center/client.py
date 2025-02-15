"""API client."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pypco import PCO

from .services import Services


class _Auth(BaseSettings):
    """Authentication."""

    model_config = SettingsConfigDict(env_file=".env")

    client_id: SecretStr
    client_secret: SecretStr


class Client:
    """API client."""

    def __init__(self) -> None:
        """Initialize client."""
        auth = _Auth()
        self._pco = PCO(
            application_id=auth.client_id.get_secret_value(),
            secret=auth.client_secret.get_secret_value(),
        )

    @property
    def services(self) -> Services:
        """Services API wrapper."""
        return Services(self._pco)
