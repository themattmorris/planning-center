"""[People endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/person).
"""

import datetime
from typing import Literal, TypedDict, Unpack

from ..base import Endpoint, PerPage, endpoint
from .models import (
    Blockout,
    BlockoutDate,
    Email,
    Person,
    PlanPerson,
    PlanPersonStatus,
    Schedule,
)


class BlockoutDates(Endpoint[BlockoutDate]):
    """Blockout dates endpoint."""

    def get(self, blockout_date_id: int, /) -> BlockoutDate:
        """Get a blockout date."""

    def list_all(self) -> list[BlockoutDate]:
        """Get all blockout dates."""


class Blockouts(Endpoint[Blockout]):
    """Blockouts endpoint."""

    def get(self, blockout_id: int, /) -> Blockout:
        """Get a blockout."""

    def list_all(
        self,
        *,
        filter: Literal["past", "future"] | None = None,
        per_page: PerPage = 25,
    ) -> list[Blockout]:
        """Get all blockouts for a person."""

    @endpoint
    def blockout_dates(self) -> BlockoutDates:
        """[Blockout dates endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/blockout_date).
        """


class Emails(Endpoint[Email]):
    """Emails endpoint."""

    def get(self, email_id: int, /) -> Email:
        """Get an email."""

    def list_all(self, *, per_page: PerPage = 25) -> list[Email]:
        """Get all emails for a person."""


type ScheduleInclude = Literal["plan_times"]


class Schedules(Endpoint[Schedule]):
    """Schedules endpoint."""

    def get(
        self,
        schedule_id: int,
        /,
        *,
        include: ScheduleInclude | None = None,
    ) -> Schedule:
        """Get a schedule."""

    def list_all(
        self,
        *,
        include: ScheduleInclude | None = None,
        filter: Literal["past", "future"] | None = None,
        per_page: PerPage = 25,
    ) -> list[Schedule]:
        """Get all schedules for a person."""


type PlanPersonInclude = Literal["declined_plan_times", "person", "plan", "team"]


class PlanPersonParams(TypedDict, total=False):
    """Parameters for creating or updating a plan person."""

    person_id: int
    team_id: int
    status: PlanPersonStatus
    decline_reason: str
    notes: str
    team_position_name: str
    responds_to_id: int
    prepare_notification: bool
    notification_prepared_at: datetime.datetime


class PlanPeople(Endpoint[PlanPerson]):
    """PlanPeople endpoint."""

    def get(
        self,
        plan_person_id: int,
        /,
        *,
        include: PlanPersonInclude | None = None,
    ) -> PlanPerson:
        """Get a plan person."""

    def list_all(
        self,
        *,
        include: PlanPersonInclude | None = None,
        per_page: PerPage = 25,
    ) -> list[PlanPerson]:
        """Get all plan people."""

    def update(
        self,
        plan_person_id: int,
        /,
        **kwargs: Unpack[PlanPersonParams],
    ) -> PlanPerson:
        """Update a plan person."""

    def delete(self, plan_person_id: int, /) -> None:
        """Delete a plan person."""


type PersonInclude = Literal["emails", "tags", "team_leaders"]


class People(Endpoint[Person]):
    """People endpoint."""

    def get(
        self,
        person_id: int,
        /,
        *,
        include: PersonInclude | None = None,
    ) -> Person:
        """Get a person."""

    def list_all(
        self,
        *,
        include: PersonInclude | None = None,
        order: Literal[
            "created_at",
            "first_name",
            "last_name",
            "updated_at",
            "-created_at",
            "-first_name",
            "-last_name",
            "-updated_at",
        ]
        | None = None,
        per_page: PerPage = 25,
    ) -> list[Person]:
        """Get all people."""

    @endpoint
    def blockouts(self) -> Blockouts:
        """[Blockouts endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/blockout).
        """

    @endpoint
    def emails(self) -> Emails:
        """[Emails endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/email).
        """

    @endpoint
    def schedules(self) -> Schedules:
        """[Schedules endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/schedule).
        """

    @endpoint
    def plan_people(self) -> PlanPeople:
        """[PlanPeople endpoint](
        https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/plan_person).
        """
