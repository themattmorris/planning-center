"""People models."""

import datetime
from typing import Any

from ..base import FrozenModel, ResponseModel
from .ids import GenderId, PrimaryCampusId


class PersonAttributes(FrozenModel):
    """Person attributes."""

    avatar: str
    """File UUID (see File Uploads section)."""

    demographic_avatar_url: str
    """URL of the demographic avatar."""

    first_name: str
    """First name of the profile."""

    name: str
    """Full name of the profile."""

    status: str
    """Set to "inactive" to set "inactivated_at" to the current time and make the
    profile inactive. Set to anything else to clear "inactivated_at" and reactivate the
    profile.
    """

    remote_id: int | None
    """Remote ID of the profile."""

    accounting_administrator: bool
    """Whether the profile is an accounting administrator."""

    anniversary: datetime.date | None
    """Anniversary date."""

    birthdate: datetime.date | None
    """Birthdate."""

    child: bool
    """Whether the profile is a child."""

    given_name: str | None
    """Given name of the profile."""

    grade: int | None
    """Grade level."""

    graduation_year: int | None
    """Year of graduation."""

    last_name: str
    """Last name of the profile."""

    middle_name: str | None
    """Middle name of the profile."""

    nickname: str | None
    """Nickname of the profile."""

    people_permissions: str | None
    """Permissions related to people."""

    site_administrator: bool
    """Whether the profile is a site administrator."""

    gender: str | None
    """Gender of the profile."""

    inactivated_at: datetime.datetime | None
    """Set to an ISO 8601 date or time to make the profile inactive. Set to "null" to
    reactivate the profile.
    """

    medical_notes: str | None
    """Medical notes for the profile."""

    membership: str | None
    """Membership status."""

    created_at: datetime.datetime
    """Date and time when the profile was created."""

    updated_at: datetime.datetime
    """Date and time when the profile was last updated."""

    can_create_forms: bool
    """Whether the profile can create forms."""

    can_email_lists: bool
    """Whether the profile can email lists."""

    directory_shared_info: dict[str, Any] | None = None
    """Directory shared information. Only available when requested with the ?fields
    param.
    """

    directory_status: str | None
    """Directory status of the profile."""

    passed_background_check: bool | None
    """Whether the profile has passed a background check."""

    resource_permission_flags: dict[str, Any] | None
    """Resource permission flags."""

    school_type: str | None
    """Type of school."""

    login_identifier: str | None = None
    """Login identifier for the profile."""

    mfa_configured: bool | None = None
    """Whether multi-factor authentication is configured. Only available when requested
    with the ?fields param. Set to "true" or "false" to filter. Can only be viewed and
    queried by an Organization Administrator.
    """

    stripe_customer_identifier: str | None = None
    """Stripe customer identifier. Only available when requested with the ?fields
    param.
    """


class PersonRelationship(FrozenModel):
    """Person relationship."""

    primary_campus: PrimaryCampusId | None = None
    gender: GenderId | None = None


class Person(ResponseModel):
    """A person record represents a single member/user of the application. Each person
    has different permissions that determine how the user can use this app (if at all).
    """

    attributes: PersonAttributes
    relationships: PersonRelationship
