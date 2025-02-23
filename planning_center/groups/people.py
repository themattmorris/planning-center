"""[People endpoint](
https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/person).
"""

import datetime
from typing import Literal

from pydantic import Field

from ..base import Endpoint, FrozenModel, PerPage, ResponseModel


class Address(FrozenModel):
    """Address attributes."""

    city: str
    line_1: str
    line_2: str | None = None
    location: str
    state: str
    street: str
    street_line_1: str
    street_line_2: str | None = None
    zip: str = Field(pattern=r"^\d{5}$")


class Email(FrozenModel):
    """Email attributes."""

    address: str
    location: str
    primary: bool


class PhoneNumber(FrozenModel):
    """Phone number attributes."""

    number: str
    carrier: str | None = None
    location: str
    primary: bool


class PersonAttributes(FrozenModel):
    """Person attributes."""

    addresses: list[Address]
    """Returns all the addresses associated with this person."""

    avatar_url: str
    """The URL of the person's avatar."""

    child: bool | None = None
    """Whether or not the person is under 13 years old. This is false if a birthdate is
    not set. Only available when requested with the ?fields param"""

    created_at: datetime.datetime
    """Date and time this person was first created in Planning Center"""

    email_addresses: list[Email]
    """Returns all the email addresses associated with this person."""

    first_name: str
    """The person's first name."""

    last_name: str
    """The person's last name."""

    permissions: str
    """Can be administrator, group_type_manager, leader, member, or no access."""

    phone_numbers: list[PhoneNumber]
    """Returns all the phone numbers associated with this person."""


class Person(ResponseModel):
    """A person is a user of Planning Center. They can be a member of a group, a leader
    of a group, or an administrator.
    """

    attributes: PersonAttributes


class People(Endpoint[Person]):
    """People endpoint."""

    def get(self, person_id: str, /) -> Person:
        """Get a person."""

    def list_all(
        self,
        *,
        order: Literal[
            "first_name",
            "last_name",
            "-first_name",
            "-last_name",
        ]
        | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        per_page: PerPage = 25,
    ) -> list[Person]:
        """Get all people."""
