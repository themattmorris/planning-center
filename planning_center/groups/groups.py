"""[Groups endpoint](
https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/group).
"""

import datetime
from typing import Literal

from pydantic import Field

from ..base import Endpoint, FrozenModel, PerPage, ResponseModel, endpoint
from .ids import EnrollmentId, GroupId, GroupTypeId, LocationId, PersonId


type Role = Literal["member", "leader"]


class Address(FrozenModel):
    """Address attributes."""

    city: str
    line_1: str
    line_2: str | None = None
    location: str
    state: str
    street: str
    street_line_1: str
    street_line_2: str | None = None
    zip: str | None = Field(pattern=r"^\d{5}(-\d{4})?$", default=None)


class Email(FrozenModel):
    """Email attributes."""

    address: str
    location: str
    primary: bool


class PhoneNumber(FrozenModel):
    """Phone number attributes."""

    number: str
    carrier: str | None = None
    location: str
    primary: bool


class PersonAttributes(FrozenModel):
    """Person attributes."""

    addresses: list[Address]
    """Returns all the addresses associated with this person."""

    avatar_url: str
    """The URL of the person's avatar."""

    child: bool | None = None
    """Whether or not the person is under 13 years old. This is false if a birthdate is
    not set. Only available when requested with the ?fields param"""

    created_at: datetime.datetime
    """Date and time this person was first created in Planning Center"""

    email_addresses: list[Email]
    """Returns all the email addresses associated with this person."""

    first_name: str
    """The person's first name."""

    last_name: str
    """The person's last name."""

    permissions: str
    """Can be administrator, group_type_manager, leader, member, or no access."""

    phone_numbers: list[PhoneNumber]
    """Returns all the phone numbers associated with this person."""


class Person(ResponseModel):
    """A person is a user of Planning Center. They can be a member of a group, a leader
    of a group, or an administrator.
    """

    attributes: PersonAttributes


class MembershipAttributes(FrozenModel):
    """Membership attributes."""

    joined_at: datetime.datetime
    role: Role


class MembershipRelationship(FrozenModel):
    """Membership relationship."""

    group: GroupId | None = None
    person: PersonId | None = None


class Membership(ResponseModel):
    """The state of a Person belonging to a Group. A Person can only have one active
    Membership to a Group at a time.
    """

    attributes: MembershipAttributes
    relationships: MembershipRelationship
    person: Person | None = None


type MembershipInclude = Literal["person"]


class Memberships(Endpoint[Membership]):
    """A membership of a person in a group."""

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


class GroupRelationship(FrozenModel):
    """Group relationship."""

    group_type: GroupTypeId
    location: LocationId | None = None
    enrollment: EnrollmentId | None = None


class GroupAttributes(FrozenModel):
    """Group attributes."""

    archived_at: datetime.datetime | None = None
    """The date and time the group was archived."""

    can_create_conversation: bool | None = None
    """A boolean representing the current user's authorization to start a new
    conversation in the group. Only available when requested with the ?fields param.
    """

    chat_enabled: bool
    """A boolean representing whether or not the group has Chat enabled."""

    contact_email: str | None = None
    """If a contact_email is provided, we will display a contact button on the public
    page where potential members can ask questions before joining the group.
    """

    created_at: datetime.datetime
    """The date and time the group was created."""

    description: str
    """A longform description of the group. Can contain HTML markup."""

    events_visibility: Literal["public", "members"]
    """The visibility of events for the group. Possible values: public or members"""

    header_image: dict[str, str]
    """A hash of header image URLs. The keys are thumbnail, medium, and original."""

    leaders_can_search_people_database: bool
    """Whether or not group leaders have access to the entire church database on the
    admin side of Groups. (Not recommended).
    """

    location_type_preference: str
    """The location type preference for the group.
    Possible values: physical or virtual"""

    memberships_count: int
    """The number of members in the group, includes leaders. Does not include membership
    requests.
    """

    name: str
    """The name/title of the group."""

    public_church_center_web_url: str | None
    """The public URL for the group on Church Center."""

    schedule: str | None = None
    """A text summary of the group's typical meeting schedule. Can be a string like
    "Sundays at 9:30am" or "Every other Tuesday at 7pm".
    """

    virtual_location_url: str | None
    """The URL for the group's virtual location. A zoom link, for example. This could be
    set even if location_type_preference is physical. This is useful if you want to
    display a zoom link even if the group is meeting in person.
    """


class Group(ResponseModel):
    """A group of people that meet together regularly."""

    attributes: GroupAttributes
    relationships: GroupRelationship


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
