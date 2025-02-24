"""[Service type endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/service_type).
"""

from __future__ import annotations

import datetime
from typing import Annotated, Any, Literal, TypedDict, Unpack

from pydantic import Field

from ..base import Endpoint, FrozenModel, PerPage, ResponseModel, endpoint
from .ids import (
    FolderId,
    PersonId,
    PlanId,
    SeriesId,
    ServiceTypeId,
    SplitTeamRehearsalAssignmentId,
    TeamId,
)
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
