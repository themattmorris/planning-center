"""API wrapper base class."""

from __future__ import annotations

import abc
import enum
import functools
import http
import inspect
from collections.abc import Callable
from types import get_original_bases
from typing import (
    Annotated,
    Any,
    Generic,
    NotRequired,
    Self,
    TypedDict,
    TypeVar,
    cast,
    final,
    get_args,
    overload,
    override,
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
    meta: MetaDict


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


class _BaseCaller(Generic[R]):
    def __init__(
        self,
        root: bool,
        func: Callable[P, R],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.endpoint = cast(Endpoint, args[0])
        self.root = root
        self.func = func
        self.args = args
        self.kwargs = {k: self._to_json(v) for k, v in kwargs.items() if v is not None}

    def _to_json(self, value: Any) -> Any:
        """Convert to a value that can be serialized to JSON."""
        if isinstance(value, list | tuple | set):
            return type(value)(self._to_json(v) for v in value)

        if isinstance(value, dict):
            return {k: self._to_json(v) for k, v in value.items()}

        if isinstance(value, BaseModel):
            return value.model_dump(by_alias=True, exclude_none=True)

        return value

    @abc.abstractmethod
    def _call_api(self, url: str) -> Response:
        """Call the API."""

    @property
    def app(self) -> App:
        return self.endpoint._app

    @staticmethod
    def _get_next(response: Response) -> str | None:
        return response["links"].get("next")

    def _get_response(self) -> Response:
        args = self.args
        endpoint_parts: list[str] = []
        url_args = [*reversed(self.endpoint._ids), *args[1:]]

        for i, parent in enumerate(
            reversed([(endpoint := self.endpoint), *endpoint._endpoints])
        ):
            endpoint_parts.append(to_snake(type(parent).__name__))
            if len(url_args) >= (i + 1):
                endpoint_parts.append(str(url_args[i]))

        url_parts = [to_snake(type(self.app).__name__), "v2", *endpoint_parts]

        if not self.root:
            url_parts.append(self.func.__name__)

        return self._call_api((sep := "/") + sep.join(url_parts))

    def run(self: _BaseCaller[R]) -> R:
        response = self._get_response()
        result = response["data"]

        if (isinstance(result, list)) and (next_page := self._get_next(response)):
            while next_page is not None:
                next_response = self._call_api(next_page)
                result.extend(next_response["data"])
                next_page = self._get_next(next_response)

        return result


@final
class _GetCaller(_BaseCaller):
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

    def _call_api(self, url: str) -> Response:
        query_params = self.query_params
        payload = {k: v for k, v in self.kwargs.items() if k not in query_params} | {
            f"where[{k}]": v for k, v in query_params.items()
        }

        return self.app._pco.get(url, **payload)


class _UpdateCaller(_BaseCaller):
    @property
    def extra_payload_data(self) -> dict[str, Any]:
        return {}

    @property
    def payload(self) -> dict[str, Any]:
        return {
            "data": {
                "attributes": self.kwargs,
                "type": get_args(get_original_bases(self.endpoint)[0])[0],  # type: ignore[arg-type]
            }
            | self.extra_payload_data
        }


@final
class _PostCaller(_UpdateCaller):
    def _call_api(self, url: str) -> Response:
        return self.app._pco.post(url, self.payload)


@final
class _PatchCaller(_UpdateCaller):
    @property
    @override
    def extra_payload_data(self) -> dict[str, Any]:
        return {"id": self.args[-1]}

    def _call_api(self, url: str) -> Response:
        return self.app._pco.patch(url, self.payload)


@final
class _DeleteCaller(_BaseCaller):
    def _call_api(self, url: str) -> Response:
        return self.app._pco.delete(url)


class HTTPMethod(enum.Enum):
    """HTTP methods."""

    GET = (http.HTTPMethod.GET, _GetCaller)
    """Retrieve the target."""

    POST = (http.HTTPMethod.POST, _PostCaller)
    """Perform target-specific processing with the request payload."""

    PATCH = (http.HTTPMethod.PATCH, _PatchCaller)
    """Apply partial modifications to a target."""

    DELETE = (http.HTTPMethod.DELETE, _DeleteCaller)
    """Remove the target."""

    def __init__(self, http_method: http.HTTPMethod, caller: type[_BaseCaller]) -> None:
        """Initialize the HTTP method."""
        self.http_method = http_method
        self.caller = caller

    def __str__(self) -> str:
        """String representation of method."""
        return str(self.http_method)

    @overload
    def __call__(self, _func: Callable[P, R]) -> Callable[P, R]: ...

    @overload
    def __call__(self, *, root: bool) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

    def __call__(
        self,
        _func: Callable[P, R] | None = None,
        *,
        root: bool = True,
    ) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
        """Decorate a method to run the corresponding HTTP method."""

        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            @validate_call(validate_return=True)
            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return self.caller(root, func, *args, **kwargs).run()  # type: ignore[arg-type]

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

    def __init__(
        self,
        app: App,
        *endpoints: Endpoint,
        ids: list[int] | None = None,
    ) -> None:
        """Initialize endpoint."""
        self._app = app
        self._endpoints = endpoints
        self._ids = ids or []

    def __call__(self, id: int) -> Self:
        """Get an item by id."""
        return type(self)(self._app, *self._endpoints, ids=[id, *self._ids])

    def __init_subclass__(cls) -> None:
        """Decorate certain methods in subclass."""
        super().__init_subclass__()
        for method, http_method in [
            (cls.get, HTTPMethod.GET),
            (cls.list_all, HTTPMethod.GET),
            (cls.create, HTTPMethod.POST),
            (cls.update, HTTPMethod.PATCH),
            (cls.delete, HTTPMethod.DELETE),
        ]:
            if not getattr(method, "__isabstractmethod__", False):
                setattr(cls, method.__name__, http_method(root=True)(method))  # type: ignore[arg-type]

    @abc.abstractmethod
    def get(self, id: int, /, *, include: str | None = None) -> M:
        """Get an item by id."""

    @abc.abstractmethod
    def list_all(
        self,
        include: str | None = None,
        order: str | None = None,
        per_page: PerPage = 25,
        filter: str | None = None,
    ) -> list[M]:
        """List all items."""

    @abc.abstractmethod
    def update(self, *args: int, **kwargs: Any) -> None:
        """Update an item."""

    @abc.abstractmethod
    def create(self, **kwargs: Any) -> None:
        """Create an item."""

    @abc.abstractmethod
    def delete(self, id: int, /) -> None:
        """Delete an item."""


class endpoint(property):  # noqa: N801
    """Property that returns an instance of the annotated type."""

    def __get__(
        self,
        instance: App | Endpoint | None,
        owner: type[App | Endpoint],
    ) -> Endpoint:
        """Return the app type."""
        if instance:
            return_type: type[Endpoint] = get_return_type(self.fget)  # type: ignore[arg-type]
            if isinstance(instance, App):
                return return_type(instance)

            return return_type(
                instance._app,
                instance,
                *instance._endpoints,
                ids=instance._ids,
            )
        return super().__get__(instance, owner)
