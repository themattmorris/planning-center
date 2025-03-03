"""[Service type endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/service_type).
"""

from __future__ import annotations

import datetime
from typing import Annotated, Any, Literal, TypedDict, Unpack

from pydantic import Field

from ..base import Endpoint, FrozenModel, PerPage, ResponseModel, endpoint
from .ids import (
    AttachmentTypeId,
    FolderId,
    PersonId,
    PlanId,
    SeriesId,
    ServiceTypeId,
    SplitTeamRehearsalAssignmentId,
    TagId,
    TeamId,
    TeamPositionId,
    TimePreferenceOptionId,
)
from .people import Person
from .teams import Team, TeamInclude


class ServiceTypeAttributes(FrozenModel):
    """Service type attributes."""

    archived_at: datetime.datetime | None
    created_at: datetime.datetime
    deleted_at: datetime.datetime | None
    name: str
    sequence: int
    updated_at: datetime.datetime
    permissions: str
    attachment_types_enabled: bool
    scheduled_publish: bool
    custom_item_types: list[Any]
    standard_item_types: list[Any]
    background_check_permissions: str
    comment_permissions: str
    frequency: str
    last_plan_from: str


class ServiceTypeRelationship(FrozenModel):
    """Service type relationship."""

    parent: FolderId | None = None


class ServiceType(ResponseModel):
    """A Service Type is a container for plans."""

    attributes: ServiceTypeAttributes
    relationships: ServiceTypeRelationship


type ServiceTypeInclude = Literal["time_preference_options"]


class PlanAttributes(FrozenModel):
    """Plan attributes."""

    can_view_order: bool
    prefers_order_view: bool
    rehearsable: bool

    items_count: int
    """The total number of items, including regular items, songs, media, and headers,
    that the current user can see in the plan.
    """

    permissions: str
    """The current user's permissions for this plan's Service Type."""

    created_at: datetime.datetime
    title: str | None
    updated_at: datetime.datetime

    public: bool
    """True if Public Access has been enabled."""

    series_title: str | None
    plan_notes_count: int
    other_time_count: int
    rehearsal_time_count: int
    service_time_count: int
    plan_people_count: int
    needed_positions_count: int

    total_length: int
    """The total of length of all items, excluding pre-service and post-service items.
    """

    multi_day: bool

    files_expire_at: datetime.datetime | None
    """A date 15 days after the last service time. Returns in the time zone specified in
    your organization's localization settings.
    """

    sort_date: datetime.datetime | None
    """A time representing the chronological first Service Time, used to sort plan
    chronologically. If no Service Times exist, it uses Rehearsal Times, then Other
    Times, then NOW. Returns in the time zone specified in your organization's
    localization settings.
    """

    last_time_at: datetime.datetime | None
    """Returns in the time zone specified in your organization's localization settings.
    """

    dates: str
    """The full date string representing all Service Time dates."""

    short_dates: str
    """The shortened date string representing all Service Time dates. Months are
    abbreviated, and the year is omitted.
    """

    planning_center_url: str
    reminders_disabled: bool


class PlanRelationship(FrozenModel):
    """Plan relationship."""

    service_type: ServiceTypeId
    previous_plan: PlanId | None = None
    next_plan: PlanId | None = None
    series: SeriesId | None = None
    created_by: PersonId | None = None
    updated_by: PersonId | None = None


class Plan(ResponseModel):
    """A single plan within a Service Type."""

    attributes: PlanAttributes
    relationships: PlanRelationship


class Plans(Endpoint[Plan]):
    """Plan endpoint."""

    def get(
        self,
        plan_id: int,
        /,
        *,
        include: Literal[
            "contributors",
            "my_schedules",
            "plan_times",
            "series",
        ]
        | None = None,
        order: Literal[
            "created_at",
            "sort_date",
            "title",
            "updated_at",
            "-created_at",
            "-sort_date",
            "-title",
            "-updated_at",
        ]
        | None = None,
        created_at: datetime.datetime | None = None,
        series_title: str | None = None,
        title: str | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> Plan:
        """Get a plan."""

    def list_all(
        self,
        *,
        include: Literal[
            "contributors",
            "my_schedules",
            "plan_times",
            "series",
        ]
        | None = None,
        order: Literal[
            "created_at",
            "sort_date",
            "title",
            "updated_at",
            "-created_at",
            "-sort_date",
            "-title",
            "-updated_at",
        ]
        | None = None,
        created_at: datetime.datetime | None = None,
        series_title: str | None = None,
        title: str | None = None,
        updated_at: datetime.datetime | None = None,
        filter: Literal["future", "no_dates", "past"] | None = None,
        per_page: PerPage = 25,
    ) -> list[Plan]:
        """Get all plans."""


class TeamReminder(FrozenModel):
    """Team reminder."""

    team_id: int
    value: Annotated[int, Field(ge=0, le=7)]

    def get_team(self, *, include: TeamInclude | None = None) -> Team:
        """Load the team."""
        return TeamId(id=self.team_id).load(include=include)


type TimeType = Literal["rehearsal", "service", "other"]


class PlanTimeAttributes(FrozenModel):
    """Plan attributes."""

    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str | None
    time_type: TimeType
    recorded: bool

    team_reminders: list[TeamReminder]
    """A Hash that maps a Team ID to a reminder value. If nothing is specified, no
    reminder is set for that team. A reminder value is an integer (0-7) equal to the
    number of days before the selected time a reminder should be sent.
    """

    starts_at: datetime.datetime
    """Planned start time."""

    ends_at: datetime.datetime
    """Planned end time."""

    live_starts_at: datetime.datetime | None
    """Start time as recorded by Services LIVE."""

    live_ends_at: datetime.datetime | None
    """End time as recorded by Services LIVE."""


class PlanTimeRelationship(FrozenModel):
    """PlanTime relationship."""

    assigned_times: list[TeamId] | None = None
    split_team_rehearsal_assignments: list[SplitTeamRehearsalAssignmentId] | None = None


class PlanTime(ResponseModel):
    """A time in a plan."""

    attributes: PlanTimeAttributes
    relationships: PlanTimeRelationship


type PlanTimeInclude = Literal["split_team_rehearsal_assignments"]


class PlanTimesParams(TypedDict, total=False):
    """Parameters for creating or updating a plan time."""

    starts_at: datetime.datetime
    ends_at: datetime.datetime
    name: str
    time_type: TimeType
    team_reminders: list[TeamReminder]


class PlanTimes(Endpoint[PlanTime]):
    """Plan time endpoint."""

    def get(
        self,
        plan_time_id: int,
        /,
        *,
        include: PlanTimeInclude | None = None,
        time_type: TimeType | None = None,
    ) -> PlanTime:
        """Get a plan time."""

    def list_all(
        self,
        *,
        include: PlanTimeInclude | None = None,
        order: Literal["starts_at", "-starts_at"] | None = None,
        time_type: TimeType | None = None,
        per_page: PerPage = 25,
    ) -> list[PlanTime]:
        """Get plan times for a service type."""

    def create(self, **kwargs: Unpack[PlanTimesParams]) -> PlanTime:
        """Create a plan time."""

    def update(
        self,
        plan_time_id: int,
        /,
        **kwargs: Unpack[PlanTimesParams],
    ) -> PlanTime:
        """Update a plan time."""

    def delete(self, plan_time_id: int, /) -> None:
        """Delete a plan time."""


class TeamPositionAttributes(FrozenModel):
    """Team position attributes."""

    name: str
    sequence: int | None = None

    tags: list[dict[str, str]] | None = None
    """If the Team is assigned via tags, these are specific Tags that are specified."""

    negative_tag_groups: list[dict[str, str]] | None = None
    """If the Team is assigned via tags, these are Tags where the option "None" is
    specified.
    """

    tag_groups: list[dict[str, str]] | None = None
    """If the Team is assigned via tags, these are Tags where the option "Any" is
    specified.
    """


class TeamPositionRelationships(FrozenModel):
    """Team position relationships."""

    team: TeamId
    attachment_types: list[AttachmentTypeId] | None = None
    tags: list[TagId] | None = None


class TeamPosition(ResponseModel):
    """Team position."""

    attributes: TeamPositionAttributes
    relationships: TeamPositionRelationships


type SchedulePreference = Literal[
    "Every week",
    "Every other week",
    "Every 3rd week",
    "Every 4th week",
    "Every 5th week",
    "Every 6th week",
    "Once a month",
    "Twice a month",
    "Three times a month",
    "Choose Weeks",
    "As often as needed",
]


class PersonTeamPositionAssignmentAttributes(FrozenModel):
    """Person team position attributes."""

    created_at: datetime.datetime
    updated_at: datetime.datetime | None = None
    schedule_preference: SchedulePreference
    preferred_weeks: list[int] | None = None
    """When schedule_preference is set to "Choose Weeks" then this indicates which weeks
    are preferred (checked). e.g. ['1', '3', '5'] to prefer odd num.
    """


class PersonTeamPositionAssignmentRelationships(FrozenModel):
    """Person team position relationships."""

    person: PersonId
    team_position: TeamPositionId
    time_preference_options: list[TimePreferenceOptionId]


class PersonTeamPositionAssignment(ResponseModel):
    """A person's assignment to a position within a team.."""

    attributes: PersonTeamPositionAssignmentAttributes
    relationships: PersonTeamPositionAssignmentRelationships
    person: Person | None = None
    team_position: TeamPosition | None = None


type PersonTeamPositionAssignmentIncludeValues = Literal["person", "team_position"]
type PersonTeamPositionAssignmentInclude = (
    PersonTeamPositionAssignmentIncludeValues
    | list[PersonTeamPositionAssignmentIncludeValues]
)


class PersonTeamPositionAssignments(Endpoint[PersonTeamPositionAssignment]):
    """Person team position endpoint."""

    def get(
        self,
        person_team_position_assignment_id: int,
        /,
        *,
        include: PersonTeamPositionAssignmentInclude | None = None,
    ) -> PersonTeamPositionAssignment:
        """Get a person team position."""

    def list_all(
        self,
        *,
        include: PersonTeamPositionAssignmentInclude | None = None,
        order: Literal[
            "first_name",
            "last_name",
            "-first_name",
            "-last_name",
        ]
        | None = None,
        per_page: PerPage = 25,
    ) -> list[PersonTeamPositionAssignment]:
        """List all person team positions."""

    def create(
        self,
        *,
        person_id: int,
        schedule_preference: SchedulePreference | None = None,
        preferred_weeks: list[int] | None = None,
        time_preference_option_ids: list[int] | None = None,
    ) -> PersonTeamPositionAssignment:
        """Create a person team position."""

    def update(
        self,
        person_team_position_assignment_id: int,
        /,
        *,
        schedule_preference: SchedulePreference | None = None,
        preferred_weeks: list[int] | None = None,
        time_preference_option_ids: list[int] | None = None,
    ) -> PersonTeamPositionAssignment:
        """Update a person team position."""

    def delete(self, person_team_position_assignment_id: int, /) -> None:
        """Delete a person team position."""


type TeamPositionInclude = Literal["tags", "team"]


class TeamPositions(Endpoint[TeamPosition]):
    """Team position endpoint."""

    def get(
        self,
        team_position_id: int,
        /,
        *,
        include: TeamPositionInclude | None = None,
    ) -> TeamPosition:
        """Get a team position."""

    def list_all(
        self,
        *,
        include: TeamPositionInclude | None = None,
        order: Literal["name", "-name"] | None = None,
        per_page: PerPage = 25,
    ) -> list[TeamPosition]:
        """List all team positions."""

    @endpoint
    def person_team_position_assignments(self) -> PersonTeamPositionAssignments:
        """[Person team position endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/person_team_position_assignment).
        """


class ServiceTypes(Endpoint[ServiceType]):
    """Service type endpoint."""

    def get(
        self,
        service_type_id: int,
        /,
        *,
        include: ServiceTypeInclude | None = None,
    ) -> ServiceType:
        """Get a service type."""

    def list_all(
        self,
        *,
        include: ServiceTypeInclude | None = None,
        order: Literal["name", "sequence", "-name", "-sequence"] | None = None,
        per_page: PerPage = 25,
        name: str | None = None,
    ) -> list[ServiceType]:
        """List all service types."""

    @endpoint
    def plans(self) -> Plans:
        """[Plan endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/plan).
        """

    @endpoint
    def plan_times(self) -> PlanTimes:
        """[Plan time endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/plan_time).
        """

    @endpoint
    def team_positions(self) -> TeamPositions:
        """[Team position endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/team_position).
        """
