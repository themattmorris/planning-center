"""Services models."""

from __future__ import annotations

import datetime
from typing import Annotated, Any, Literal

from pydantic import Field

from ..base import FrozenModel, ResponseModel
from .ids import (
    AttachmentTypeId,
    BlockoutId,
    FolderId,
    OrganizationId,
    PersonId,
    PersonTeamPositionAssignmentId,
    PlanId,
    PlanNoteCategoryId,
    PlanPersonId,
    PlanTimeId,
    SeriesId,
    ServiceTypeId,
    SplitTeamRehearsalAssignmentId,
    TagId,
    TeamId,
    TeamPositionId,
    TimePreferenceOptionId,
)


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


type TeamInclude = Literal[
    "people",
    "person_team_position_assignments",
    "service_type",
    "team_leaders",
    "team_positions",
]


class TeamReminder(FrozenModel):
    """Team reminder."""

    team_id: int
    value: Annotated[int, Field(ge=0, le=7)]

    def get_team(self, *, include: TeamInclude | None = None) -> Team:
        """Load the team."""
        return TeamId(id=self.team_id).load(include=include)


type TimeType = Literal["rehearsal", "service", "other"]


class PlanTimeAttributes(FrozenModel):
    """Plan attributes."""

    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str | None
    time_type: TimeType
    recorded: bool

    team_reminders: list[TeamReminder]
    """A Hash that maps a Team ID to a reminder value. If nothing is specified, no
    reminder is set for that team. A reminder value is an integer (0-7) equal to the
    number of days before the selected time a reminder should be sent.
    """

    starts_at: datetime.datetime
    """Planned start time."""

    ends_at: datetime.datetime
    """Planned end time."""

    live_starts_at: datetime.datetime | None
    """Start time as recorded by Services LIVE."""

    live_ends_at: datetime.datetime | None
    """End time as recorded by Services LIVE."""


class PlanTimeRelationship(FrozenModel):
    """PlanTime relationship."""

    assigned_times: list[TeamId] | None = None
    split_team_rehearsal_assignments: list[SplitTeamRehearsalAssignmentId] | None = None


class PlanTime(ResponseModel):
    """A time in a plan."""

    attributes: PlanTimeAttributes
    relationships: PlanTimeRelationship


class PlanTemplateAttributes(FrozenModel):
    """PlanTemplate attributes."""

    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    item_count: int
    team_count: int
    note_count: int
    can_view_order: bool
    multi_day: bool
    rehearsable: bool
    prefers_order_view: bool


class PlanTemplateRelationship(FrozenModel):
    """PlanTemplate relationship."""

    service_type: ServiceTypeId
    created_by: PersonId
    updated_by: PersonId | None


class PlanTemplate(ResponseModel):
    """A PlanTemplate Resource."""

    attributes: PlanTemplateAttributes
    relationships: PlanTemplateRelationship


class PlanNoteAttributes(FrozenModel):
    """PlanNote attributes."""

    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    category_name: str
    content: str


class PlanNoteRelationship(FrozenModel):
    """PlanNote relationship."""

    created_by: PersonId
    plan_note_category: PlanNoteCategoryId
    teams: list[TeamId]


class PlanNote(ResponseModel):
    """A specific plan note within a single plan."""

    attributes: PlanNoteAttributes
    relationships: PlanNoteRelationship


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
    created_by: PersonId | None = None
    updated_by: PersonId | None = None


class Plan(ResponseModel):
    """A single plan within a Service Type."""

    attributes: PlanAttributes
    relationships: PlanRelationship
    plan_times: list[PlanTime] | None = None


class TimePreferenceOptionAttributes(FrozenModel):
    """Time preference option attributes."""

    day_of_week: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: str
    sort_index: str
    time_type: str
    minute_of_day: int
    starts_at: datetime.datetime


class TimePreferenceOption(ResponseModel):
    """A Service Time a person prefers to be scheduled to."""

    attributes: TimePreferenceOptionAttributes


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


class BlockoutDateAttributes(FrozenModel):
    """Blockout date attributes."""

    group_identifier: str
    reason: str | None
    time_zone: str
    share: bool
    starts_at: datetime.datetime
    ends_at: datetime.datetime
    ends_at_utc: datetime.datetime
    starts_at_utc: datetime.datetime


class BlockoutDateRelationship(FrozenModel):
    """Blockout date relationship."""

    person: PersonId
    blockout: BlockoutId


class BlockoutDate(ResponseModel):
    """The actual dates generated by the blockout or its recurrence pattern. Generated
    up to a year in advance.
    """

    attributes: BlockoutDateAttributes
    relationships: BlockoutDateRelationship


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


class NeededPositionAttributes(FrozenModel):
    """Needed position attributes."""

    quantity: int
    team_position_name: str
    scheduled_to: str


class NeededPositionRelationship(FrozenModel):
    """Needed position relationship."""

    team: TeamId
    plan: PlanId
    time: PlanTimeId | None = None
    time_preference_option: TimePreferenceOptionId | None = None


class NeededPosition(ResponseModel):
    """An amount of unfilled positions needed within a team in a plan."""

    attributes: NeededPositionAttributes
    relationships: NeededPositionRelationship


type PlanPersonStatus = Literal["C", "U", "D", "Confirmed", "Unconfirmed", "Declined"]


class PlanPersonAttributes(FrozenModel):
    """PlanPerson attributes."""

    status: PlanPersonStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    notes: str | None
    decline_reason: str | None
    name: str
    notification_changed_by_name: str | None
    notification_sender_name: str | None
    team_position_name: str
    photo_thumbnail: str

    scheduled_by_name: str | None = None
    """Only available when requested with the ?fields param."""

    status_updated_at: datetime.datetime | None = None
    notification_changed_at: datetime.datetime | None = None
    notification_prepared_at: datetime.datetime | None = None
    notification_read_at: datetime.datetime | None = None
    notification_sent_at: datetime.datetime | None = None
    prepare_notification: bool

    can_accept_partial: bool
    """If the person is scheduled to a split team where they could potentially accept 1
    time and decline another.
    """


class PlanPersonRelationship(FrozenModel):
    """PlanPerson relationship."""

    person: PersonId
    plan: PlanId
    scheduled_by: PersonId
    service_type: ServiceTypeId
    team: TeamId
    responds_to: PersonId | None = None
    times: list[PlanTimeId]
    time_preference_options: list[TimePreferenceOptionId] | None = None


class PlanPerson(ResponseModel):
    """A person scheduled within a specific plan."""

    attributes: PlanPersonAttributes
    relationships: PlanPersonRelationship


class SchedulingPreferenceAttributes(FrozenModel):
    """Scheduling preference attributes."""

    preference: str


class SchedulingPreferenceRelationship(FrozenModel):
    """Scheduling preference relationship."""

    household_member: PersonId


class SchedulingPreference(ResponseModel):
    """Household member scheduling preference."""

    attributes: SchedulingPreferenceAttributes
    relationships: SchedulingPreferenceRelationship


class TeamPositionAttributes(FrozenModel):
    """Team position attributes."""

    name: str
    sequence: int | None = None

    tags: list[dict[str, str]] | None = None
    """If the Team is assigned via tags, these are specific Tags that are specified."""

    negative_tag_groups: list[dict[str, str]] | None = None
    """If the Team is assigned via tags, these are Tags where the option "None" is
    specified.
    """

    tag_groups: list[dict[str, str]] | None = None
    """If the Team is assigned via tags, these are Tags where the option "Any" is
    specified.
    """


class TeamPositionRelationships(FrozenModel):
    """Team position relationships."""

    team: TeamId
    attachment_types: list[AttachmentTypeId] | None = None
    tags: list[TagId] | None = None


class TeamPosition(ResponseModel):
    """Team position."""

    attributes: TeamPositionAttributes
    relationships: TeamPositionRelationships


type SchedulePreference = Literal[
    "Every week",
    "Every other week",
    "Every 3rd week",
    "Every 4th week",
    "Every 5th week",
    "Every 6th week",
    "Once a month",
    "Twice a month",
    "Three times a month",
    "Choose Weeks",
    "As often as needed",
]


class PersonTeamPositionAssignmentAttributes(FrozenModel):
    """Person team position attributes."""

    created_at: datetime.datetime
    updated_at: datetime.datetime | None = None
    schedule_preference: SchedulePreference
    preferred_weeks: list[int] | None = None
    """When schedule_preference is set to "Choose Weeks" then this indicates which weeks
    are preferred (checked). e.g. ['1', '3', '5'] to prefer odd num.
    """


class PersonTeamPositionAssignmentRelationships(FrozenModel):
    """Person team position relationships."""

    person: PersonId
    team_position: TeamPositionId
    time_preference_options: list[TimePreferenceOptionId]


class PersonTeamPositionAssignment(ResponseModel):
    """A person's assignment to a position within a team.."""

    attributes: PersonTeamPositionAssignmentAttributes
    relationships: PersonTeamPositionAssignmentRelationships
    person: Person | None = None
    team_position: TeamPosition | None = None


class TeamRelationship(FrozenModel):
    """Team relationship."""

    service_type: ServiceTypeId
    default_responds_to: PersonId
    person_team_position_assignments: list[PersonTeamPositionAssignmentId] | None = None
    team_positions: list[TeamPositionId] | None = None
    people: list[PersonId] | None = None


class TeamAttributes(FrozenModel):
    """Team attributes."""

    name: str
    rehearsal_team: bool
    sequence: int | None

    schedule_to: Literal["plan", "time"]
    """This determines whether a team is a split team or not."""

    default_status: str
    default_prepare_notifications: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    archived_at: datetime.datetime | None
    viewers_see: int
    assigned_directly: bool
    secure_team: bool
    last_plan_from: str
    stage_color: str
    stage_variant: str | None


class Team(ResponseModel):
    """A team within a service type."""

    attributes: TeamAttributes
    relationships: TeamRelationship
    people: list[Person] | None = None
    person_team_position_assignments: list[PersonTeamPositionAssignment] | None = None
    service_type: ServiceType | None = None
    team_leaders: list[Person] | None = None
    team_positions: list[TeamPosition] | None = None
