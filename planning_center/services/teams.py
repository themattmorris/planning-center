"""[Teams endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/team).
"""

import datetime
from typing import Literal

from ..base import Endpoint, FrozenModel, PerPage, ResponseModel
from .ids import PersonId, PersonTeamPositionAssignmentId, ServiceTypeId


class TeamRelationship(FrozenModel):
    """Team relationship."""

    service_type: ServiceTypeId
    default_responds_to: PersonId
    person_team_position_assignments: list[PersonTeamPositionAssignmentId] | None = None
    people: list[PersonId] | None = None


class TeamAttributes(FrozenModel):
    """Team attributes."""

    name: str
    rehearsal_team: bool
    sequence: int | None

    schedule_to: Literal["plan", "time"]
    """This determines whether a team is a split team or not."""

    default_status: str
    default_prepare_notifications: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    archived_at: datetime.datetime | None
    viewers_see: int
    assigned_directly: bool
    secure_team: bool
    last_plan_from: str
    stage_color: str
    stage_variant: str | None


class Team(ResponseModel):
    """A team within a service type."""

    attributes: TeamAttributes
    relationships: TeamRelationship


type TeamInclude = Literal[
    "people",
    "person_team_position_assignments",
    "service_type",
    "team_leaders",
    "team_positions",
]


class Teams(Endpoint[Team]):
    """Teams endpoint."""

    def get(
        self,
        team_id: int,
        /,
        *,
        include: TeamInclude | None = None,
    ) -> Team:
        """Get a team."""

    def list_all(
        self,
        *,
        include: TeamInclude | None = None,
        order: Literal[
            "created_at",
            "name",
            "updated_at",
            "-created_at",
            "-name",
            "-updated_at",
        ]
        | None = None,
        name: str | None = None,
        per_page: PerPage = 25,
    ) -> list[Team]:
        """List all teams."""
