"""API wrapper base class."""

import enum
import functools
import http
from collections.abc import Callable
from typing import Any, NotRequired, Self, TypedDict, cast, overload

from pydantic import BaseModel, ConfigDict, TypeAdapter, model_validator, validate_call
from pypco import PCO

from ._typing import P, R, get_return_type


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


class DataDict(TypedDict):
    """Data about a related attribute."""

    id: int
    type: str


class LinksDict(TypedDict):
    """Links portion of response."""

    self: str
    next: NotRequired[str]


class NextDict(TypedDict):
    """Next page."""

    offset: int


class MetaDict(TypedDict):
    """Meta portion of response."""

    total_count: int
    count: int
    next: NotRequired[NextDict]
    can_order_by: list[str]
    can_query_by: list[str]
    can_include: list[str]
    parent: DataDict


class Response(TypedDict):
    """Response from the planning center API."""

    links: LinksDict
    data: Any
    included: list[str]


class FrozenModel(BaseModel):
    """A pydantic BaseModel that is immutable."""

    model_config = ConfigDict(frozen=True, validate_default=True, extra="ignore")


class ResponseModel(FrozenModel):
    """Response model with generic validation."""

    @model_validator(mode="before")
    @classmethod
    def _get_relationships(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Remove any relationships that are empty."""
        if relationships := values.pop(key := "relationships", None):
            values[key] = {
                k: data for k, v in relationships.items() if (data := v.get("data"))
            }

        return values

    @classmethod
    def get(cls, id: int) -> Self:
        """Get an instance of self by id."""
        # TODO: implement


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

    @staticmethod
    def _get_next(response: Response) -> str | None:
        return response["links"].get("next")

    @overload
    def __call__(self, _func: Callable[P, R]) -> Callable[P, R]: ...

    @overload
    def __call__(self, *, root: bool) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

    def __call__(
        self,
        _func: Callable[P, R] | None = None,
        *,
        root: bool = False,
    ) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
        """Decorate a method to run the corresponding HTTP method."""

        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            @validate_call
            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                endpoint = cast(Endpoint, args[0])
                app = endpoint._app

                def _run_it(url: str) -> Response:
                    return app._pco.request_json(
                        self.value,
                        url,
                        **{k: v for k, v in kwargs.items() if v is not None},
                    )

                url_parts = [
                    type(app).__name__.lower(),
                    "v2",
                    type(endpoint).__name__.lower(),
                    *(str(arg) for arg in args[1:]),
                ]

                if not root:
                    url_parts.append(func.__name__.lower())

                response = _run_it((sep := "/") + sep.join(url_parts))
                result = response["data"]

                if (isinstance(result, list)) and (
                    next_page := self._get_next(response)
                ):
                    while next_page is not None:
                        next_response = _run_it(next_page)
                        result.extend(next_response["data"])
                        next_page = self._get_next(next_response)

                # Convert result to annotated BaseModel
                adapter = TypeAdapter(get_return_type(func))
                return cast(R, adapter.validate_python(result))

            return wrapper

        return decorator(_func) if _func else decorator


class endpoint_property(property):  # noqa: N801
    """Property that returns an instance of the annotated type."""

    def __get__(self, instance: App | None, owner: type[App]) -> Endpoint:  # type: ignore[override]
        """Return the app type."""
        if instance:
            return_type: type[Endpoint] = get_return_type(self.fget)  # type: ignore[arg-type]
            return return_type(instance)
        return super().__get__(instance, owner)
