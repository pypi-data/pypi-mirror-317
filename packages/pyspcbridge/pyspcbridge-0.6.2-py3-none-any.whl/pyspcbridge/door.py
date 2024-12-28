import logging

from .const import DoorMode
from .spc_error import SpcError
from .utils import _load_enum

_LOGGER = logging.getLogger(__name__)


class Door:
    """Represents a SPC door lock."""

    def __init__(self, bridge, spc_door):
        self._bridge = bridge
        self._id = spc_door.get("id")
        self._name = spc_door.get("name")
        self._values = {
            "mode": _load_enum(DoorMode, spc_door.get("mode", 0)),
            "entry_granted_user": "",
            "entry_denied_user": "",
            "exit_granted_user": "",
            "exit_denied_user": "",
        }
        self._http_client = bridge._http_client

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def entry_granted(self):
        return self._values["entry_granted_user"]

    @property
    def entry_denied(self):
        return self._values["entry_denied_user"]

    @property
    def exit_granted(self):
        return self._values["exit_granted_user"]

    @property
    def exit_denied(self):
        return self._values["exit_denied_user"]

    @property
    def mode(self):
        return self._values["mode"]

    def change_values(self, values) -> list:
        changed_values = []

        for k, v in values.items():
            value = v
            if k == "mode":
                value = _load_enum(DoorMode, v)
            if value != self._values[k]:
                self._values[k] = value
                changed_values.append(k)

        return changed_values

    async def async_command(self, command, code) -> dict:
        if code is None:
            return SpcError(54).error

        username = None
        password = None
        username, password = self._bridge.get_user_credentials(code)
        if username is None or password is None:
            return SpcError(54).error

        return await self._http_client.async_command_door(
            command, self._id, username, password
        )
