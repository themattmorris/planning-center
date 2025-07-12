"""API wrapper base class."""

from __future__ import annotations

import abc
import datetime
import enum
import functools
import http
import inspect
from collections.abc import Callable
from types import get_original_bases
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Literal,
    NotRequired,
    Self,
    TypedDict,
    TypeVar,
    cast,
    final,
    get_args,
    get_origin,
    overload,
    override,
)

import requests
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    model_validator,
    validate_call,
)
from pydantic.alias_generators import to_snake
from pypco import PCO

from ._typing import P, R, T, get_return_type
from .utils import to_PascalCase


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
    included: list[dict[str, Any]] | dict[str, Any]
    relationships: dict[str, dict[Literal["data"], DataDict | list[DataDict]]]
    meta: MetaDict


class FrozenModel(BaseModel):
    """A pydantic BaseModel that is immutable."""

    model_config = ConfigDict(frozen=True, validate_default=True, extra="ignore")


def validate(value: Any, hint: type[T]) -> T:
    """Perform validation on a value according to a type hint."""
    adapter = TypeAdapter(hint)
    return adapter.validate_python(value)


class ResponseModel(FrozenModel):
    """Response model with generic validation."""

    id: int

    @model_validator(mode="before")
    @classmethod
    def _get_relationships(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Remove any relationships that are empty."""
        if relationships := values.get(key := "relationships"):
            values[key] = {
                k: data
                for k, v in relationships.items()
                if isinstance(v, dict) and ((data := v.get("data")) is not None)
            }

        return values


class _BaseCaller[R]:
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
        self.kwargs = {
            k: (
                ",".join(v)
                if (k == "include") and isinstance(v, list)
                else self._to_json(v)
            )
            for k, v in kwargs.items()
            if v is not None
        }

    def _to_json(self, value: Any) -> Any:
        """Convert to a value that can be serialized to JSON."""
        if isinstance(value, list | tuple | set):
            return type(value)(self._to_json(v) for v in value)

        if isinstance(value, dict):
            return {k: self._to_json(v) for k, v in value.items()}

        if isinstance(value, BaseModel):
            return value.model_dump(by_alias=True, exclude_none=True)

        if isinstance(value, datetime.date):
            return value.isoformat()

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
        url_args: list[str] = []

        for parent in self.endpoint._parents:
            url_args.extend([parent.endpoint.name, str(parent.id)])

        url_parts = [
            self.app.name,
            "v2",
            *url_args,
            self.endpoint.name,
            *[str(arg) for arg in self.args[1:]],
        ]

        if not self.root:
            url_parts.append(self.func.__name__)

        return self._call_api((sep := "/") + sep.join(url_parts))

    def _get_id(
        self,
        response: Response | list[Response],
        include_string: str,
    ) -> int | list[int]:
        if isinstance(response, list):
            return [self._get_id(r, include_string) for r in response]

        result = response["relationships"][include_string]["data"]

        if isinstance(result, list):
            return [r["id"] for r in result]

        return result["id"]

    def _parse_response(  # noqa: PLR0912
        self,
        response: Response | requests.Response,
    ) -> dict[str, Any] | list[dict[str, Any]] | None:
        if isinstance(response, dict):
            result = response["data"]

            if include := response.get("included"):
                for include_string in self.kwargs["include"].split(","):
                    if isinstance(include, list):
                        if isinstance(
                            item_id := self._get_id(result, include_string),
                            list,
                        ) and isinstance(result, dict):
                            return result | {include_string: include}

                        id_key = "id"
                        for included in include:
                            included_id = included[id_key]
                            if isinstance(result, list):
                                for i, item in enumerate(result):
                                    item_id = self._get_id(item, include_string)
                                    if isinstance(item_id, list):
                                        if included_id in item_id:
                                            if include_string not in item:
                                                result[i][include_string] = [included]
                                            else:
                                                item[include_string].append(included)
                                    elif included[id_key] == item_id:
                                        result[i][include_string] = included
                                        break
                            elif isinstance(item_id, list):
                                if included_id in item_id:
                                    result[include_string] = included
                            elif included_id == item_id:
                                result[include_string] = included
                    else:
                        result[include_string] = include

            return result

        return None

    def run(self: _BaseCaller[R]) -> R:
        response = self._get_response()
        result = self._parse_response(response)

        if (isinstance(result, list)) and (next_page := self._get_next(response)):
            while next_page is not None:
                next_response = self._call_api(next_page)
                result.extend(
                    cast(list[dict[str, Any]], self._parse_response(next_response))
                )
                next_page = self._get_next(next_response)

        # This will be validated by pydantic
        return result  # type: ignore[return-value]


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


class _UpdateCaller(_BaseCaller[R]):
    @property
    def extra_payload_data(self) -> dict[str, Any]:
        return {}

    @property
    def payload(self) -> dict[str, Any]:
        kwargs = dict(self.kwargs)

        # Determine if any of the kwargs are relationships.
        relationships: dict[str, Any] = {}

        for k, v in inspect.signature(self.func).parameters.items():
            if (annotation := v.annotation) is Relationship:
                type_name = to_PascalCase(k)
                as_list = False

            elif (
                (get_origin(v.annotation) is Annotated)
                and (metadata := annotation.__metadata__)
                and isinstance(first := metadata[0], RelationshipInfo)
            ):
                type_name = first.type_name
                as_list = first.as_list
            else:
                type_name = None

                if (annotation is not inspect.Parameter.empty) and (k in kwargs):
                    kwargs[k] = validate(kwargs[k], annotation)

            if type_name and ((value := kwargs.pop(k, None)) is not None):
                relationship_data: DataDict | list[DataDict] = DataDict(
                    type=type_name,
                    id=cast(int, value),
                )

                if as_list:
                    relationship_data = [relationship_data]

                relationships[k] = {"data": relationship_data}

        data = {
            "type": get_args(get_original_bases(type(self.endpoint))[0])[0].__name__,
            "attributes": kwargs,
        }

        if relationships:
            data["relationships"] = relationships

        return {"data": data | self.extra_payload_data}


@final
class _PostCaller(_UpdateCaller[R]):
    def _call_api(self, url: str) -> Response:
        return self.app._pco.post(url, self.payload)

    @override
    def run(self: _PostCaller[R]) -> R:
        response = cast(dict[str, Any], super().run())
        return_type = get_return_type(self.func)
        return validate(response, return_type)


@final
class _PatchCaller(_UpdateCaller[R]):
    @property
    @override
    def extra_payload_data(self) -> dict[str, Any]:
        return {"id": self.args[-1]}

    def _call_api(self, url: str) -> Response:
        return self.app._pco.patch(url, self.payload)


@final
class _DeleteCaller(_BaseCaller[R]):
    def _call_api(self, url: str) -> Response:
        return self.app._pco.delete(url)


class HTTPMethod(enum.Enum):
    """HTTP methods."""

    GET = (http.HTTPMethod.GET, _GetCaller, True)
    """Retrieve the target."""

    POST = (http.HTTPMethod.POST, _PostCaller, False)
    """Perform target-specific processing with the request payload."""

    PATCH = (http.HTTPMethod.PATCH, _PatchCaller, True)
    """Apply partial modifications to a target."""

    DELETE = (http.HTTPMethod.DELETE, _DeleteCaller, True)
    """Remove the target."""

    def __init__(
        self,
        http_method: http.HTTPMethod,
        caller: type[_BaseCaller],
        validate: bool,
    ) -> None:
        """Initialize the HTTP method."""
        self.http_method = http_method
        self.caller = caller
        self.validate = validate

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
            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return self.caller(root, func, *args, **kwargs).run()  # type: ignore[arg-type]

            return (
                validate_call(validate_return=True)(wrapper)
                if self.validate
                else wrapper
            )

        return decorator(_func) if _func else decorator


class RelationshipInfo(FrozenModel):
    """Metadata to indicate that an attribute is a relationship."""

    type_name: str
    as_list: bool


if TYPE_CHECKING:
    Relationship = int
else:

    class Relationship:
        """Sentinel value for relationship annotations."""


def _to_url_name(value: Any) -> str:
    return to_snake(value.__name__)


class _EndpointBase:
    @property
    def name(self) -> str:
        return _to_url_name(type(self))


class App(_EndpointBase):
    """Base class for planning center app."""

    def __init__(self, pco: PCO) -> None:
        """Initialize app."""
        self._pco = pco


M = TypeVar("M", bound=ResponseModel)


type PerPage = Annotated[int, Field(ge=1, le=100)]


class Endpoint[M](_EndpointBase):
    """Base class for planning center endpoint."""

    def __init__(self, app: App, *parents: _Parent) -> None:
        """Initialize endpoint."""
        self._app = app
        self._parents = list(parents)

    def __call__(self, id: int) -> Self:
        """Get an item by id."""
        self._parents.append(_Parent(endpoint=self, id=id))
        return self

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
        raise NotImplementedError

    @abc.abstractmethod
    def list_all(
        self,
        include: str | None = None,
        order: str | None = None,
        per_page: PerPage = 25,
        filter: str | None = None,
    ) -> list[M]:
        """List all items."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *args: int, **kwargs: Any) -> M:
        """Update an item."""
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, **kwargs: Any) -> M:
        """Create an item."""
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id: int, /) -> None:
        """Delete an item."""
        raise NotImplementedError


class endpoint(property):  # noqa: N801
    """Property that returns an instance of the annotated type."""

    def __get__(
        self,
        instance: App | Endpoint | None,
        owner: type[App | Endpoint],
    ) -> Endpoint:
        """Return the app/endpoint type."""
        if instance:
            return_type: type[Endpoint] = get_return_type(self.fget)  # type: ignore[arg-type]
            if isinstance(instance, App):
                return return_type(instance)

            # Ensure that the parent endpoint id has been provided.
            parents = instance._parents
            if not any(isinstance(parent.endpoint, owner) for parent in parents):
                message = (
                    f"Must provide ID for {(name := _to_url_name(owner))} endpoint. "
                    f"Hint: `.{name}(12345).{_to_url_name(return_type)}`"
                )
                raise ValueError(message)

            return return_type(instance._app, *parents)
        return super().__get__(instance, owner)


class _Parent(FrozenModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    endpoint: Endpoint
    id: int


class Related(FrozenModel):
    """Data about a related attribute."""

    id: int

    @model_validator(mode="before")
    @classmethod
    def _drop_type(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Remove the type from the data."""
        if (data_type := values.get("type")) and (
            data_type != (expected := cls.__name__.removesuffix("Id"))
        ):
            message = f"Expected type {expected!r} but got {data_type!r}."
            raise ValueError(message)

        return values
