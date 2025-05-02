"""Planning center [groups](https://developer.planning.center/docs/#/apps/groups) API."""  # noqa: E501

from ..base import App, endpoint
from .group_types import GroupTypes
from .groups import Groups as GroupsEndpoint
from .groups import People


class Groups(App):
    """Groups API wrapper."""

    @endpoint
    def groups(self) -> GroupsEndpoint:
        """[Groups endpoint](
        https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/group).
        """

    @endpoint
    def group_types(self) -> GroupTypes:
        """[Group types endpoint](
        https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/group_type).
        """

    @endpoint
    def people(self) -> People:
        """[People endpoint](
        https://developer.planning.center/docs/#/apps/groups/2023-07-10/vertices/person).
        """
