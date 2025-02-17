"""API wrapper base class."""

from __future__ import annotations

import abc
import enum
import functools
import http
import inspect
from collections.abc import Callable
from typing import (
    Annotated,
    Any,
    Generic,
    NotRequired,
    Self,
    TypedDict,
    TypeVar,
    cast,
    overload,
)

from pydantic import BaseModel, ConfigDict, Field, model_validator, validate_call
from pydantic.alias_generators import to_snake
from pypco import PCO

from ._typing import P, R, get_return_type


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

    id: int

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


class _OutputParser(Generic[R]):
    def __init__(
        self,
        method: HTTPMethod,
        root: bool,
        func: Callable[P, R],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.endpoint = cast(Endpoint, args[0])
        self.method = method
        self.root = root
        self.func = func
        self.args = args
        self.kwargs = {k: v for k, v in kwargs.items() if v is not None}

    @property
    def app(self) -> App:
        return self.endpoint._app

    @property
    def query_params(self) -> dict[str, Any]:
        """Extra query params that are filters."""
        if (kwargs := self.kwargs) and (
            abstract_method := getattr(Endpoint, self.func.__name__, None)
        ):
            return {
                k: v
                for k, v in kwargs.items()
                if k not in inspect.signature(abstract_method).parameters
            }

        return {}

    @staticmethod
    def _get_next(response: Response) -> str | None:
        return response["links"].get("next")

    def _call_api(self, url: str) -> Response:
        query_params = self.query_params
        return self.app._pco.request_json(
            self.method.value,
            url,
            **{k: v for k, v in self.kwargs.items() if k not in query_params}
            | {f"where[{k}]": v for k, v in query_params.items()},
        )

    def _get_response(self) -> Response:
        url_parts = [
            to_snake(type(self.app).__name__),
            "v2",
            to_snake(type(self.endpoint).__name__),
            *(str(arg) for arg in self.args[1:]),
        ]

        if not self.root:
            url_parts.append(self.func.__name__)

        return self._call_api((sep := "/") + sep.join(url_parts))

    def run(self: _OutputParser[R]) -> R:
        response = self._get_response()
        result = response["data"]

        if (isinstance(result, list)) and (next_page := self._get_next(response)):
            while next_page is not None:
                next_response = self._call_api(next_page)
                result.extend(next_response["data"])
                next_page = self._get_next(next_response)

        return result


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
            @validate_call(validate_return=True)
            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                output_parser = _OutputParser(self, root, func, *args, **kwargs)
                return output_parser.run()

            return wrapper

        return decorator(_func) if _func else decorator


class App:
    """Base class for planning center app."""

    def __init__(self, pco: PCO) -> None:
        """Initialize app."""
        self._pco = pco


M = TypeVar("M", bound=ResponseModel)


type PerPage = Annotated[int, Field(ge=1, le=100)]


class Endpoint(Generic[M]):
    """Base class for planning center endpoint."""

    def __init__(self, app: App) -> None:
        """Initialize endpoint."""
        self._app = app

    def __init_subclass__(cls) -> None:
        """Decorate certain methods in subclass."""
        super().__init_subclass__()
        cls.get = HTTPMethod.GET(root=True)(cls.get)  # type: ignore[method-assign]
        cls.list_all = HTTPMethod.GET(root=True)(cls.list_all)  # type: ignore[method-assign]

    @abc.abstractmethod
    def get(self, id: int, /, *, include: str | None = None) -> M:
        """Get an item by id."""

    @abc.abstractmethod
    def list_all(
        self,
        include: str | None = None,
        order: str | None = None,
        per_page: PerPage = 25,
    ) -> list[M]:
        """List all items."""


class endpoint_property(property):  # noqa: N801
    """Property that returns an instance of the annotated type."""

    def __get__(self, instance: App | None, owner: type[App]) -> Endpoint:  # type: ignore[override]
        """Return the app type."""
        if instance:
            return_type: type[Endpoint] = get_return_type(self.fget)  # type: ignore[arg-type]
            return return_type(instance)
        return super().__get__(instance, owner)
