"""[Teams endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/team).
"""

from typing import Literal

from ..base import Endpoint, PerPage
from .models import Team, TeamInclude


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
