"""Relationship id types."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import model_validator

from ..base import FrozenModel


if TYPE_CHECKING:
    from . import Services
    from .people import Person, PersonInclude
    from .service_types import ServiceType, ServiceTypeInclude
    from .teams import Team, TeamInclude


class Data(FrozenModel):
    """Data about a related attribute."""

    id: int

    @model_validator(mode="before")
    @classmethod
    def _drop_type(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Remove the type from the data."""
        if (data_type := values.pop("type", None)) and (
            data_type != (expected := cls.__name__.removesuffix("Id"))
        ):
            message = f"Expected type {expected!r} but got {data_type!r}."
            raise ValueError(message)

        return values

    @property
    def _services(self) -> Services:
        from ..client import Client

        return Client().services


class FolderId(Data):
    """Folder id."""


class PlanId(Data):
    """Plan id."""


class OrganizationId(Data):
    """Organization id."""


class PersonId(Data):
    """Person id."""

    def load(self, *, include: PersonInclude | None = None) -> Person:
        """Load the person."""
        return self._services.people.get(self.id, include=include)


class PlanPersonId(Data):
    """Plan person id."""


class PlanTimeId(Data):
    """Plan time id."""


class PersonTeamPositionAssignmentId(Data):
    """Person team position assignment id."""


class BlockoutId(Data):
    """Blockout id."""


class SeriesId(Data):
    """Series id."""


class ServiceTypeId(Data):
    """Service type id."""

    def load(self, *, include: ServiceTypeInclude | None = None) -> ServiceType:
        """Load the person."""
        return self._services.service_types.get(self.id, include=include)


class TeamId(Data):
    """Team id."""

    def load(self, *, include: TeamInclude | None = None) -> Team:
        """Load the person."""
        return self._services.teams.get(self.id, include=include)


class SplitTeamRehearsalAssignmentId(Data):
    """Split team rehearsal assignment id."""


class TimePreferenceOptionId(Data):
    """Time preference option id."""
