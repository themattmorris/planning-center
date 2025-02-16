"""Relationship id types."""

from typing import Any

from pydantic import model_validator

from ..base import FrozenModel


class Data(FrozenModel):
    """Data about a related attribute."""

    id: int

    @model_validator(mode="before")
    @classmethod
    def _drop_type(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Remove the type from the data."""
        if (data_type := values.pop("type")) != (
            expected := cls.__name__.removesuffix("Id")
        ):
            message = f"Expected type {expected!r} but got {data_type!r}."
            raise ValueError(message)

        return values


class FolderId(Data):
    """Folder id."""


class PlanId(Data):
    """Plan id."""


class OrganizationId(Data):
    """Organization id."""


class PersonId(Data):
    """Person id."""


class PlanPersonId(Data):
    """Plan person id."""


class SeriesId(Data):
    """Series id."""


class ServiceTypeId(Data):
    """Service type id."""


class TeamId(Data):
    """Team id."""
