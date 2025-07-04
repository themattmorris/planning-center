"""[Service type endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/service_type).
"""

import datetime
from typing import Literal, TypedDict, Unpack

from ..base import Endpoint, PerPage, endpoint
from .models import (
    NeededPosition,
    PersonTeamPositionAssignment,
    Plan,
    PlanNote,
    PlanPerson,
    PlanTemplate,
    PlanTime,
    SchedulePreference,
    ServiceType,
    TeamPosition,
    TeamReminder,
    TimeType,
)
from .people import PlanPersonParams


type TeamMemberFilter = Literal[
    "confirmed",
    "not_archived",
    "not_declined",
    "not_deleted",
]


class TeamMembers(Endpoint[PlanPerson]):
    """Team members endpoint."""

    def get(
        self,
        plan_person_id: int,
        /,
        *,
        filter: TeamMemberFilter | None = None,
    ) -> PlanPerson:
        """Get a plan person."""

    def list_all(
        self,
        *,
        filter: TeamMemberFilter | None = None,
        per_page: PerPage = 25,
    ) -> list[PlanPerson]:
        """List all plan people."""

    def create(self, **kwargs: Unpack[PlanPersonParams]) -> PlanPerson:
        """Create a plan person."""

    def delete(self, plan_person_id: int, /) -> None:
        """Delete a plan person."""


type NeededPositionInclude = Literal["team", "time"]


class NeededPositions(Endpoint[NeededPosition]):
    """Needed positions endpoint."""

    def get(
        self,
        needed_position_id: int,
        /,
        *,
        include: NeededPositionInclude | None = None,
    ) -> NeededPosition:
        """Get a needed position."""

    def list_all(
        self,
        *,
        include: NeededPositionInclude | None = None,
        per_page: PerPage = 25,
    ) -> list[NeededPosition]:
        """List all needed positions."""

    def create(
        self,
        *,
        quantity: int | None = None,
        time_id: int | None = None,
        time_preference_option_id: int | None = None,
    ) -> NeededPosition:
        """Create a needed position."""

    def update(self, needed_position_id: int, /, quantity: int) -> NeededPosition:
        """Update a needed position."""

    def delete(self, needed_position_id: int, /) -> None:
        """Delete a needed position."""


class NotesParams(TypedDict):
    """Parameters for creating notes."""

    category_name: str
    content: str


class Notes(Endpoint):
    """Plan notes endpoint."""

    def create(self, **kwargs: Unpack[NotesParams]) -> PlanNote:
        """Create a plan note."""


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

    @endpoint
    def needed_positions(self) -> NeededPositions:
        """[Needed positions endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/needed_position).
        """

    @endpoint
    def notes(self) -> Notes:
        """Notes endpoint for creating [plan notes](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/plan_note).
        """


type PlanTemplateOrder = Literal[
    "created_at",
    "item_count",
    "name",
    "note_count",
    "team_count",
    "updated_at",
]


class PlanTemplates(Endpoint[PlanTemplate]):
    """Plan template endpoint."""

    def get(self, plan_template_id: int, /) -> PlanTemplate:
        """Get a plan template."""

    def list_all(
        self, *, order: PlanTemplateOrder | None = None, per_page: PerPage = 25
    ) -> list[PlanTemplate]:
        """Get plan templates for a service type."""


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


type ServiceTypeInclude = Literal["time_preference_options"]


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
    def plan_templates(self) -> PlanTemplates:
        """[Plan template endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/plan_template).
        """

    @endpoint
    def team_positions(self) -> TeamPositions:
        """[Team position endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/team_position).
        """
