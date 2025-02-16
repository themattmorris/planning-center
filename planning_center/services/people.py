"""[People endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/person).
"""

import datetime
from typing import Any, Literal

from ..base import Endpoint, FrozenModel, HTTPMethod, PerPage, ResponseModel
from .ids import (
    FolderId,
    OrganizationId,
    PersonId,
    PlanId,
    PlanPersonId,
    ServiceTypeId,
    TeamId,
)


class PersonRelationship(FrozenModel):
    """Person relationship."""

    created_by: PersonId | None = None
    updated_by: PersonId | None = None
    current_folder: FolderId


class PersonAttributes(FrozenModel):
    """Person attributes."""

    photo_url: str
    photo_thumbnail_url: str
    preferred_app: str
    assigned_to_rehearsal_team: bool
    archived_at: datetime.datetime | None
    created_at: datetime.datetime
    first_name: str
    last_name: str
    name_prefix: str | None
    name_suffix: str | None
    updated_at: datetime.datetime
    full_name: str
    permissions: str
    status: str
    max_permissions: str
    anniversary: datetime.date | None
    birthdate: datetime.date | None
    given_name: str | None
    middle_name: str | None
    nickname: str | None
    media_permissions: str | None = None
    song_permissions: str | None = None
    archived: bool
    site_administrator: bool
    logged_in_at: datetime.datetime | None
    notes: str | None
    passed_background_check: bool
    ical_code: str
    access_media_attachments: bool
    access_plan_attachments: bool
    access_song_attachments: bool
    preferred_max_plans_per_day: int | None
    preferred_max_plans_per_month: int | None
    praise_charts_enabled: bool | None = None
    me_tab: str | None = None
    plans_tab: str | None = None
    songs_tab: str | None = None
    media_tab: str | None = None
    people_tab: str | None = None
    can_edit_all_people: bool | None = None
    can_view_all_people: bool | None = None
    onboardings: list[Any] | None = None


class PersonLinks(FrozenModel):
    """Person links."""

    assign_tags: str | None = None
    available_signups: str | None = None
    blockouts: str | None = None
    collapse_service_types: str | None = None
    emails: str | None = None
    expand_service_types: str | None = None
    html: str | None = None
    person_team_position_assignments: str | None = None
    plan_people: str | None = None
    schedules: str | None = None
    scheduling_preferences: str | None = None
    self: str | None = None
    tags: str | None = None
    team_leaders: str | None = None
    text_settings: str | None = None


class Person(ResponseModel):
    """A person added to Planning Center Services."""

    attributes: PersonAttributes
    relationships: PersonRelationship
    links: PersonLinks | None = None


class BlockoutAttributes(FrozenModel):
    """Blockout attributes."""

    description: str
    group_identifier: str | None
    organization_name: str
    reason: str | None
    repeat_frequency: Literal[
        "no_repeat",
        "every_1",
        "every_2",
        "every_3",
        "every_4",
        "every_5",
        "every_6",
        "every_7",
        "every_8",
    ]
    repeat_interval: (
        Literal[
            "exact_day_of_month",
            "week_of_month_1",
            "week_of_month_2",
            "week_of_month_3",
            "week_of_month_4",
            "week_of_month_last",
        ]
        | None
    )
    repeat_period: Literal["daily", "weekly", "monthly", "yearly"] | None
    settings: str | None
    time_zone: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    repeat_until: datetime.date | None
    starts_at: datetime.datetime
    ends_at: datetime.datetime
    share: bool


class BlockoutRelationship(FrozenModel):
    """Blockout relationship."""

    person: PersonId
    organization: OrganizationId


class Blockout(ResponseModel):
    """An object representing a blockout date, and an optional recurrence pattern."""

    attributes: BlockoutAttributes
    relationships: BlockoutRelationship


class EmailAttributes(FrozenModel):
    """Email attributes."""

    primary: bool
    address: str


class Email(ResponseModel):
    """An email address for a person."""

    attributes: EmailAttributes


class ScheduleAttributes(FrozenModel):
    """Schedule attributes."""

    sort_date: datetime.datetime
    dates: str
    decline_reason: str | None
    organization_name: str
    organization_time_zone: str
    organization_twenty_four_hour_time: bool
    person_name: str
    position_display_times: str | None
    responds_to_name: str
    service_type_name: str
    short_dates: str
    status: str
    team_name: str
    team_position_name: str
    can_accept_partial: bool
    can_accept_partial_one_time: bool
    can_rehearse: bool

    plan_visible: bool
    """True if the scheduled Plan is visible to the scheduled Person."""

    plan_visible_to_me: bool
    """True if the scheduled Plan is visible to the current Person."""


class ScheduleRelationship(FrozenModel):
    """Schedule relationship."""

    person: PersonId
    service_type: ServiceTypeId
    organization: OrganizationId
    plan_person: PlanPersonId
    plan: PlanId
    team: TeamId
    responds_to_person: PersonId | None = None


class Schedule(ResponseModel):
    """An instance of a PlanPerson with included data for displaying in a user's
    schedule.
    """

    attributes: ScheduleAttributes
    relationships: ScheduleRelationship


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

    @HTTPMethod.GET
    def blockouts(
        self,
        person_id: int,
        /,
        *,
        filter: Literal["past", "future"] | None = None,
    ) -> list[Blockout]:
        """Get blockouts for a person."""

    @HTTPMethod.GET
    def emails(
        self,
        person_id: int,
        /,
        *,
        per_page: PerPage = 25,
    ) -> list[Email]:
        """Get emails for a person."""

    @HTTPMethod.GET
    def schedules(
        self,
        person_id: int,
        /,
        *,
        include: Literal["plan_times"] | None = None,
        order: Literal["starts_at", "-starts_at"] | None = None,
        per_page: PerPage = 25,
    ) -> list[Schedule]:
        """Get schedules for a person."""
