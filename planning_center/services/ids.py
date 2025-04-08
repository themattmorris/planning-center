"""Relationship id types."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Related


if TYPE_CHECKING:
    from . import Services
    from .models import TeamInclude
    from .people import Person, PersonInclude
    from .service_types import ServiceType, ServiceTypeInclude
    from .teams import Team


class _ServicesId(Related):
    @property
    def _services(self) -> Services:
        from ..client import Client

        return Client().services


class AttachmentTypeId(_ServicesId):
    """Attachment type id."""

    id: int | None = None  # type: ignore[assignment]


class FolderId(_ServicesId):
    """Folder id."""


class PlanId(_ServicesId):
    """Plan id."""


class OrganizationId(_ServicesId):
    """Organization id."""


class PersonId(_ServicesId):
    """Person id."""

    def load(self, *, include: PersonInclude | None = None) -> Person:
        """Load the person."""
        return self._services.people.get(self.id, include=include)


class PlanPersonId(_ServicesId):
    """Plan person id."""


class PlanTimeId(_ServicesId):
    """Plan time id."""


class PersonTeamPositionAssignmentId(_ServicesId):
    """Person team position assignment id."""


class BlockoutId(_ServicesId):
    """Blockout id."""


class SeriesId(_ServicesId):
    """Series id."""


class ServiceTypeId(_ServicesId):
    """Service type id."""

    def load(self, *, include: ServiceTypeInclude | None = None) -> ServiceType:
        """Load the person."""
        return self._services.service_types.get(self.id, include=include)


class TeamId(_ServicesId):
    """Team id."""

    def load(self, *, include: TeamInclude | None = None) -> Team:
        """Load the person."""
        return self._services.teams.get(self.id, include=include)


class TeamPositionId(_ServicesId):
    """Team position id."""


class SplitTeamRehearsalAssignmentId(_ServicesId):
    """Split team rehearsal assignment id."""


class TimePreferenceOptionId(_ServicesId):
    """Time preference option id."""


class TagId(_ServicesId):
    """Tag id."""
