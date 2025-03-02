"""Relationship id types."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Related


if TYPE_CHECKING:
    from . import People


class _PeopleId(Related):
    @property
    def _groups(self) -> People:
        from ..client import Client

        return Client().people


class PrimaryCampusId(_PeopleId):
    """Primary Campus ID."""


class GenderId(_PeopleId):
    """Gender ID."""
