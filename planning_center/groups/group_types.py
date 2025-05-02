"""[Group types endpoint](
https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/group_type).
"""

from typing import Literal

from ..base import Endpoint, PerPage, endpoint
from .models import GroupType, Resource


class Resources(Endpoint[Resource]):
    """Resources endpoint."""

    def get(self, resource_id: int, /) -> Resource:
        """Get a resource."""

    def list_all(
        self,
        *,
        order: Literal["name", "-name", "last_updated", "-last_updated"] | None = None,
        per_page: PerPage = 25,
    ) -> list[Resource]:
        """Get all resources."""


class GroupTypes(Endpoint[GroupType]):
    """Group types endpoint."""

    def get(self, group_type_id: int, /) -> GroupType:
        """Get a group type."""

    def list_all(
        self,
        *,
        order: Literal["name", "position", "-name", "-position"] | None = None,
        per_page: PerPage = 25,
    ) -> list[GroupType]:
        """Get all group types."""

    @endpoint
    def resources(self) -> Resources:
        """[Resources endpoint](
        https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/resource).
        """
