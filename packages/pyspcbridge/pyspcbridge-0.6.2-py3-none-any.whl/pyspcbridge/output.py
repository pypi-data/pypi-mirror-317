import logging

from .spc_error import SpcError

_LOGGER = logging.getLogger(__name__)


class Output:
    """Represents a SPC output/mapping gate."""

    def __init__(self, bridge, spc_output):
        self._bridge = bridge
        self._id = spc_output.get("id")
        self._name = spc_output.get("name")
        self._values = {
            "state": spc_output.get("state", 0) == 1,
        }
        self._http_client = bridge._http_client

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def state(self) -> bool:
        return self._values["state"]

    def change_values(self, values) -> list:
        changed_values = []

        if values.get("state") is not None:
            if values["state"] != self._values["state"]:
                self._values["state"] = values["state"]
                changed_values.append("state")

        return changed_values

    async def async_command(self, command, code) -> dict:
        if code is None:
            return SpcError(54).error

        username = None
        password = None
        username, password = self._bridge.get_user_credentials(code)
        if username is None or password is None:
            return SpcError(54).error

        return await self._http_client.async_command_output(
            command, self._id, username, password
        )
