"""Relationship id types."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Data


if TYPE_CHECKING:
    from . import Groups


class _GroupsId(Data):
    @property
    def _groups(self) -> Groups:
        from ..client import Client

        return Client().groups


class GroupTypeId(_GroupsId):
    """Group type ID."""


class LocationId(_GroupsId):
    """Location ID."""


class EnrollmentId(_GroupsId):
    """Enrollment ID."""
