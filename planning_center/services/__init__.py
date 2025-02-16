"""Planning center [services](
https://developer.planning.center/docs/#/apps/services/2018-11-01) API.
"""

from ..base import App, endpoint_property
from .people import People
from .service_types import ServiceTypes


class Services(App):
    """Services API wrapper."""

    @endpoint_property
    def people(self) -> People:
        """People API wrapper."""

    @endpoint_property
    def service_types(self) -> ServiceTypes:
        """Service types API wrapper."""
