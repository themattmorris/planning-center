"""Planning center [people](https://developer.planning.center/docs/#/apps/people) API."""  # noqa: E501

from ..base import App, endpoint
from .people import People as PeopleEndpoint


class People(App):
    """People API wrapper."""

    @endpoint
    def people(self) -> PeopleEndpoint:
        """[People endpoint](
        https://developer.planning.center/docs/#/apps/people/2024-09-12/vertices/person).
        """
