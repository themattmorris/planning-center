"""Planning center [services](
https://developer.planning.center/docs/#/apps/services/2018-11-01) API.
"""

from ..base import App
from .people import People


class Services(App):
    """Services API wrapper."""

    @property
    def people(self) -> People:
        """People API wrapper."""
        return People(self)
