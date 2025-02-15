"""[People endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/person).
"""

import datetime
from typing import Any, Self

from pydantic import model_validator

from ..base import Endpoint, FrozenModel, HTTPMethod


class Data(FrozenModel):
    """Data about a related attribute."""

    type: str
    id: int

    @model_validator(mode="before")
    @classmethod
    def from_nested(cls, v: dict[str, dict[str, str]]) -> Self:
        """Convert nested dict to Data."""
        return cls(**v["data"])


class Relationship(FrozenModel):
    """Peron relationship."""

    created_by: Data
    updated_by: Data
    current_folder: Data


class Person(FrozenModel):
    """A person added to Planning Center Services."""

    id: int
    photo_url: str
    photo_thumbnail_url: str
    preferred_app: str
    assigned_to_rehearsal_team: bool
    archived_at: datetime.datetime | None = None
    created_at: datetime.datetime
    first_name: str
    last_name: str
    name_prefix: str
    name_suffix: str
    updated_at: datetime.datetime
    full_name: str
    permissions: str
    status: str
    max_permissions: str
    anniversary: str | None = None
    birthdate: str | None = None
    given_name: str
    middle_name: str
    nickname: str
    media_permissions: str
    song_permissions: str
    archived: bool
    site_administrator: bool
    logged_in_at: datetime.datetime | None = None
    notes: str
    passed_background_check: bool
    ical_code: str
    access_media_attachments: bool
    access_plan_attachments: bool
    access_song_attachments: bool
    preferred_max_plans_per_day: int
    preferred_max_plans_per_month: int
    praise_charts_enabled: bool
    me_tab: str
    plans_tab: str
    songs_tab: str
    media_tab: str
    people_tab: str
    can_edit_all_people: bool
    can_view_all_people: bool
    onboardings: list[Any]


class People(Endpoint):
    """People endpoint."""

    @HTTPMethod.GET
    def get(self) -> list[Person]:
        """Get all people."""
