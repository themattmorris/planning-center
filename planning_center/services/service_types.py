"""[Service type endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/service_type).
"""

import datetime
from typing import Literal, TypedDict, Unpack

from ..base import Endpoint, PerPage, endpoint
from .models import (
    PersonTeamPositionAssignment,
    Plan,
    PlanPerson,
    PlanTime,
    SchedulePreference,
    ServiceType,
    TeamPosition,
    TeamReminder,
    TimeType,
)
from .people import PlanPersonParams


type ServiceTypeInclude = Literal["time_preference_options"]


class TeamMembers(Endpoint[PlanPerson]):
    """Team members endpoint."""

    def get(
        self,
        plan_person_id: int,
        /,
        *,
        filter: Literal["confirmed", "not_archived", "not_declined", "not_deleted"]
        | None = None,
    ) -> PlanPerson:
        """Get a plan person."""

    def create(self, **kwargs: Unpack[PlanPersonParams]) -> PlanPerson:
        """Create a plan person."""


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

    @endpoint
    def team_members(self) -> TeamMembers:
        """Team members endpoint."""


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
