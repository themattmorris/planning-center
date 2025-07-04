"""Relationship id types."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Related


if TYPE_CHECKING:
    from . import Groups


class _GroupsId(Related):
    @property
    def _groups(self) -> Groups:
        from ..client import Client  # noqa: PLC0415

        return Client().groups


class GroupId(_GroupsId):
    """Group ID."""


class GroupTypeId(_GroupsId):
    """Group type ID."""


class LocationId(_GroupsId):
    """Location ID."""


class EnrollmentId(_GroupsId):
    """Enrollment ID."""


class PersonId(_GroupsId):
    """Person ID."""
