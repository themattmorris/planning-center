"""Planning center [services](
https://developer.planning.center/docs/#/apps/services/2018-11-01) API.
"""

from ..base import App, endpoint
from .people import People
from .service_types import ServiceTypes
from .teams import Teams


class Services(App):
    """Services API wrapper."""

    @endpoint
    def people(self) -> People:
        """People API wrapper."""

    @endpoint
    def service_types(self) -> ServiceTypes:
        """Service types API wrapper."""

    @endpoint
    def teams(self) -> Teams:
        """Teams API wrapper."""
