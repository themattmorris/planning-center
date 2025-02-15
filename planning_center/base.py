"""API wrapper base class."""

import enum
import functools
import http
from collections.abc import Callable
from typing import cast, get_type_hints

from pydantic import BaseModel, ConfigDict, TypeAdapter
from pypco import PCO

from ._typing import P, R


class App:
    """Base class for planning center app."""

    def __init__(self, pco: PCO) -> None:
        """Initialize app."""
        self._pco = pco


class Endpoint:
    """Base class for planning center endpoint."""

    def __init__(self, app: App) -> None:
        """Initialize endpoint."""
        self._app = app


class FrozenModel(BaseModel):
    """A pydantic BaseModel that is immutable."""

    model_config = ConfigDict(frozen=True, validate_default=True, extra="ignore")


class HTTPMethod(enum.Enum):
    """HTTP methods."""

    GET = http.HTTPMethod.GET
    """Retrieve the target."""

    POST = http.HTTPMethod.POST
    """Perform target-specific processing with the request payload."""

    PUT = http.HTTPMethod.PUT
    """Replace the target with the request payload."""

    PATCH = http.HTTPMethod.PATCH
    """Apply partial modifications to a target."""

    DELETE = http.HTTPMethod.DELETE
    """Remove the target."""

    def __str__(self) -> str:
        """String representation of method."""
        return str(self.value)

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorate a method to run the corresponding HTTP method."""

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            endpoint = cast(Endpoint, args[0])
            result = (app := endpoint._app)._pco.request_json(
                self.value,
                f"/{type(app).__name__.lower()}/v2/{type(endpoint).__name__.lower()}",
                **kwargs,
            )

            # Convert result to annotated BaseModel
            adapter = TypeAdapter(get_type_hints(func)["return"])
            return cast(R, adapter.validate_python(result["data"]))

        return wrapper
