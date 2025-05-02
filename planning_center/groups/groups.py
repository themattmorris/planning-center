"""[Groups endpoint](
https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/group).
"""

import datetime
from typing import Literal

from ..base import Endpoint, PerPage, endpoint
from .group_types import Resources
from .models import Group, Membership, Person, Role


type MembershipInclude = Literal["person"]


class Memberships(Endpoint[Membership]):
    """Memberships endpoint."""

    def get(
        self,
        membership_id: int,
        /,
        *,
        include: MembershipInclude | None = None,
    ) -> Membership:
        """Get a membership."""

    def list_all(
        self,
        *,
        include: MembershipInclude | None = None,
        order: Literal[
            "first_name",
            "joined_at",
            "last_name",
            "role",
            "-first_name",
            "-joined_at",
            "-last_name",
            "-role",
        ]
        | None = None,
        role: Role | None = None,
        per_page: PerPage = 25,
    ) -> list[Membership]:
        """Get all memberships."""

    def create(
        self,
        *,
        person_id: int,
        role: Role | None = None,
        joined_at: datetime.datetime | None = None,
    ) -> Membership:
        """Create a membership."""

    def update(
        self,
        membership_id: int,
        /,
        *,
        joined_at: datetime.datetime | None = None,
        role: Role | None = None,
    ) -> Membership:
        """Update a membership."""

    def delete(self, membership_id: int, /) -> None:
        """Delete a membership."""


type GroupInclude = Literal["enrollment", "group_type", "location"]


class Groups(Endpoint[Group]):
    """Groups endpoint."""

    def get(self, group_id: int, /, *, include: GroupInclude | None = None) -> Group:
        """Get a group."""

    def list_all(
        self,
        *,
        include: GroupInclude | None = None,
        order: Literal["name", "-name"] | None = None,
        archive_status: Literal["not_archived", "only", "include"] | None = None,
        name: str | None = None,
        per_page: PerPage = 25,
    ) -> list[Group]:
        """Get all groups."""

    @endpoint
    def memberships(self) -> Memberships:
        """[Memberships endpoint](
        https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/membership).
        """

    @endpoint
    def resources(self) -> Resources:
        """[Resources endpoint](
        https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/resource).
        """


class People(Endpoint[Person]):
    """People endpoint."""

    def get(self, person_id: int, /) -> Person:
        """Get a person."""

    def list_all(
        self,
        *,
        order: Literal[
            "first_name",
            "last_name",
            "-first_name",
            "-last_name",
        ]
        | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        per_page: PerPage = 25,
    ) -> list[Person]:
        """Get all people."""

    @endpoint
    def groups(self) -> Groups:
        """[Groups endpoint](
        https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/group).
        """
