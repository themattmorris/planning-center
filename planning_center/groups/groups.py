"""[Groups endpoint](
https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/group).
"""

import datetime
from typing import Literal

from ..base import Endpoint, FrozenModel, PerPage, ResponseModel
from ..ids import EnrollmentId, GroupTypeId, LocationId


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

    events_visibility: str
    """The visibility of events for the group.
    Possible values: public or members"""

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
