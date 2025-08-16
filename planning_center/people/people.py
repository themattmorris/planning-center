"""[People endpoint](
https://developer.planning.center/docs/#/apps/people/2024-09-12/vertices/person).
"""

import datetime
from typing import Literal, TypedDict, Unpack

from ..base import Endpoint, PerPage, get_pco
from .models import Person


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

    def import_(self):  # type: ignore[no-untyped-def]
        """Import the person."""
        pco = get_pco(api_base="https://services.planningcenteronline.com")
        return pco.post(f"/people/{self._parents[0].id}/import")
