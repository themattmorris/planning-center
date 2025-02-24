"""[People endpoint](
https://developer.planning.center/docs/#/apps/people/2024-09-12/vertices/person).
"""

import datetime
from typing import Any, Literal, TypedDict, Unpack

from ..base import Endpoint, FrozenModel, PerPage, ResponseModel
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


type PeopleInclude = Literal[
    "addresses",
    "emails",
    "field_data",
    "households",
    "inactive_reason",
    "marital_status",
    "name_prefix",
    "name_suffix",
    "organization",
    "person_apps",
    "phone_numbers",
    "platform_notifications",
    "primary_campus",
    "school",
    "social_profiles",
]


class PeopleParams(TypedDict, total=False):
    """Parameters for creating or updating a person."""

    accounting_administrator: bool
    anniversary: datetime.date
    birthdate: datetime.date
    child: bool
    first_name: str
    gender: str
    given_name: str
    grade: int
    graduation_year: int
    inactivated_at: datetime.datetime
    last_name: str
    medical_notes: str
    membership: str
    middle_name: str
    nickname: str
    people_permissions: str
    remote_id: int
    site_administrator: bool
    status: str


class People(Endpoint[Person]):
    """People endpoint."""

    def get(self, person_id: int, /, *, include: PeopleInclude | None = None) -> Person:
        """Get a person."""

    def list_all(
        self,
        *,
        include: PeopleInclude | None = None,
        order: Literal[
            "accounting_administrator",
            "anniversary",
            "birthdate",
            "child",
            "created_at",
            "first_name",
            "gender",
            "given_name",
            "grade",
            "graduation_year",
            "inactivated_at",
            "last_name",
            "membership",
            "middle_name",
            "nickname",
            "people_permissions",
            "remote_id",
            "site_administrator",
            "status",
            "updated_at",
            "-accounting_administrator",
            "-anniversary",
            "-birthdate",
            "-child",
            "-created_at",
            "-first_name",
            "-gender",
            "-given",
            "-grade",
            "-graduation_year",
            "-inactivated_at",
            "-last_name",
            "-membership",
            "-middle_name",
            "-nickname",
            "-people_permissions",
            "-remote_id",
            "-site_administrator",
            "-status",
            "-updated_at",
        ]
        | None = None,
        per_page: PerPage = 25,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
        mfa_configured: bool | None = None,
        search_name: str | None = None,
        search_name_or_email: str | None = None,
        search_name_or_email_or_phone_number: str | None = None,
        search_phone_number: str | None = None,
        search_phone_number_e164: str | None = None,
        **kwargs: Unpack[PeopleParams],
    ) -> list[Person]:
        """List all people."""

    def create(self, **kwargs: Unpack[PeopleParams]) -> Person:
        """Create a person."""

    def update(self, person_id: int, /, **kwargs: Unpack[PeopleParams]) -> Person:
        """Update a person."""

    def delete(self, person_id: int, /) -> None:
        """Delete a person."""
