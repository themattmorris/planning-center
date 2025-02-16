"""[Organization endpoint](
https://developer.planning.center/docs/#/apps/services/2018-11-01/vertices/organization).
"""

import datetime

from ..base import FrozenModel, ResponseModel


class OrganizationAttributes(FrozenModel):
    """Organization attributes."""

    ccli: str
    created_at: datetime.datetime
    date_format: int
    music_stand_enabled: bool
    name: str
    projector_enabled: bool
    time_zone: str
    twenty_four_hour_time: bool
    updated_at: datetime.datetime | None
    owner_name: str
    required_to_set_download_permissions: str
    secret: str
    allow_mp3_download: bool
    calendar_starts_on_sunday: bool
    ccli_connected: bool
    ccli_auto_reporting_enabled: bool
    ccli_reporting_enabled: bool
    extra_file_storage_allowed: bool
    file_storage_exceeded: bool
    file_storage_size: int
    file_storage_size_used: int
    file_storage_extra_enabled: bool
    rehearsal_mix_enabled: bool
    rehearsal_pack_connected: bool
    legacy_id: str
    file_storage_extra_charges: int
    people_allowed: int
    people_remaining: int
    beta: bool


class Organization(ResponseModel):
    """The root level of an organization where account-level settings are applied."""

    attributes: OrganizationAttributes
