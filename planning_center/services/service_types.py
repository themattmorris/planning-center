"""[Service type endpoint](
https://developer.planning.cente"=r/docs/#/apps/services/2018-11-01/vertices/service_type).
"""

from __future__ import annotations

import datetime
from typing import Any, Literal

from ..base import Endpoint, FrozenModel, HTTPMethod, PerPage, ResponseModel
from .ids import FolderId, PersonId, PlanId, SeriesId, ServiceTypeId


class ServiceTypeAttributes(FrozenModel):
    """Service type attributes."""

    archived_at: datetime.datetime | None
    created_at: datetime.datetime
    deleted_at: datetime.datetime | None
    name: str
    sequence: int
    updated_at: datetime.datetime
    permissions: str
    attachment_types_enabled: bool
    scheduled_publish: bool
    custom_item_types: list[Any]
    standard_item_types: list[Any]
    background_check_permissions: str
    comment_permissions: str
    frequency: str
    last_plan_from: str


class ServiceTypeRelationship(FrozenModel):
    """Service type relationship."""

    parent: FolderId | None = None


class ServiceType(ResponseModel):
    """A Service Type is a container for plans."""

    attributes: ServiceTypeAttributes
    relationships: ServiceTypeRelationship


type ServiceTypeInclude = Literal["time_preference_options"]


class PlanAttributes(FrozenModel):
    """Plan attributes."""

    can_view_order: bool
    prefers_order_view: bool
    rehearsable: bool

    items_count: int
    """The total number of items, including regular items, songs, media, and headers,
    that the current user can see in the plan.
    """

    permissions: str
    """The current user's permissions for this plan's Service Type."""

    created_at: datetime.datetime
    title: str | None
    updated_at: datetime.datetime

    public: bool
    """True if Public Access has been enabled."""

    series_title: str | None
    plan_notes_count: int
    other_time_count: int
    rehearsal_time_count: int
    service_time_count: int
    plan_people_count: int
    needed_positions_count: int

    total_length: int
    """The total of length of all items, excluding pre-service and post-service items.
    """

    multi_day: bool

    files_expire_at: datetime.datetime | None
    """A date 15 days after the last service time. Returns in the time zone specified in
    your organization's localization settings.
    """

    sort_date: datetime.datetime | None
    """A time representing the chronological first Service Time, used to sort plan
    chronologically. If no Service Times exist, it uses Rehearsal Times, then Other
    Times, then NOW. Returns in the time zone specified in your organization's
    localization settings.
    """

    last_time_at: datetime.datetime | None
    """Returns in the time zone specified in your organization's localization settings.
    """

    dates: str
    """The full date string representing all Service Time dates."""

    short_dates: str
    """The shortened date string representing all Service Time dates. Months are
    abbreviated, and the year is omitted.
    """

    planning_center_url: str
    reminders_disabled: bool


class PlanRelationship(FrozenModel):
    """Plan relationship."""

    service_type: ServiceTypeId
    previous_plan: PlanId | None = None
    next_plan: PlanId | None = None
    series: SeriesId | None = None
    created_by: PersonId
    updated_by: PersonId


class Plan(ResponseModel):
    """A single plan within a Service Type."""

    attributes: PlanAttributes
    relationships: PlanRelationship


class ServiceTypes(Endpoint[ServiceType]):
    """Service type endpoint."""

    def get(
        self,
        service_type_id: int,
        /,
        *,
        include: ServiceTypeInclude | None = None,
    ) -> ServiceType:
        """Get a service type."""

    def list_all(
        self,
        *,
        include: ServiceTypeInclude | None = None,
        order: Literal["name", "sequence", "-name", "-sequence"] | None = None,
        per_page: PerPage = 25,
        name: str | None = None,
    ) -> list[ServiceType]:
        """List all service types."""

    @HTTPMethod.GET
    def plans(  # noqa: PLR0913
        self,
        service_type_id: int,
        /,
        *,
        include: Literal[
            "contributors",
            "my_schedules",
            "plan_times",
            "series",
        ]
        | None = None,
        order: Literal[
            "created_at",
            "sort_date",
            "title",
            "updated_at",
            "-created_at",
            "-sort_date",
            "-title",
            "-updated_at",
        ]
        | None = None,
        filter: Literal["future", "no_dates", "past"] | None = None,
        per_page: PerPage = 25,
        created_at: datetime.datetime | None = None,
        series_title: str | None = None,
        title: str | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> list[Plan]:
        """Get plans for a service type."""
