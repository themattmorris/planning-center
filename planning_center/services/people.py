"""[People endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/person).
"""

import datetime
from typing import Annotated, Any, Literal

from pydantic import Field

from ..base import Endpoint, FrozenModel, HTTPMethod, ResponseModel


class Data(FrozenModel):
    """Data about a related attribute."""

    type: str
    id: int


class PersonRelationship(FrozenModel):
    """Person relationship."""

    created_by: Data | None = None
    updated_by: Data
    current_folder: Data


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

    assign_tags: str
    available_signups: str
    blockouts: str
    collapse_service_types: str
    emails: str
    expand_service_types: str
    html: str
    person_team_position_assignments: str
    plan_people: str
    schedules: str
    scheduling_preferences: str
    self: str
    tags: str
    team_leaders: str
    text_settings: str


class Person(ResponseModel):
    """A person added to Planning Center Services."""

    id: int
    attributes: PersonAttributes
    relationships: PersonRelationship
    links: PersonLinks


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

    person: Data
    organization: Data


class Blockout(ResponseModel):
    """An object representing a blockout date, and an optional recurrence pattern."""

    id: int
    attributes: BlockoutAttributes
    relationships: BlockoutRelationship


class People(Endpoint):
    """People endpoint."""

    @HTTPMethod.GET(root=True)
    def get(self, person_id: int, /) -> Person:
        """Get a person."""

    @HTTPMethod.GET(root=True)
    def list_all(
        self,
        *,
        order_by: Literal[
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
        per_page: Annotated[int, Field(ge=1, le=100)] = 25,
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
