import logging

from .const import ArmMode
from .spc_error import SpcError
from .utils import _load_enum

_LOGGER = logging.getLogger(__name__)


class Area:
    """Represents a SPC area."""

    def __init__(self, bridge, area_data):
        self._bridge = bridge
        self._id = area_data.get("id")
        self._name = area_data.get("name")
        self._a_enabled = area_data.get("a_enabled")
        self._a_name = area_data.get("a_name")
        self._b_enabled = area_data.get("b_enabled")
        self._b_name = area_data.get("b_name")
        self._exittime = area_data.get("exittime", 0)
        self._entrytime = area_data.get("entrytime", 0)
        self._http_client = bridge._http_client
        self._values = {
            "mode": _load_enum(ArmMode, area_data.get("mode")),
            "set_user": area_data.get("set_user"),
            "unset_user": area_data.get("unset_user"),
            "changed_by": "",
            "pending_exit": False,
        }
        self.zones = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def a_enabled(self):
        return self._a_enabled

    @property
    def a_name(self):
        return self._a_name

    @property
    def b_enabled(self):
        return self._b_enabled

    @property
    def b_name(self):
        return self._b_name

    @property
    def exittime(self):
        return self._exittime

    @property
    def entrytime(self):
        return self._entrytime

    @property
    def mode(self):
        return self._values["mode"]

    @mode.setter
    def mode(self, mode):
        self._values["mode"] = _load_enum(ArmMode, mode)

    @property
    def changed_by(self):
        return self._values["changed_by"]

    @property
    def set_user(self):
        return self._values["set_user"]

    @property
    def unset_user(self):
        return self._values["unset_user"]

    @property
    def pending_exit(self):
        return self._values["pending_exit"]

    @property
    def values(self):
        return self._values

    def change_values(self, values) -> list:
        changed_values = []

        if values.get("mode") is not None:
            new_mode = _load_enum(ArmMode, values["mode"])
            if new_mode != self._values["mode"]:
                self._values["mode"] = new_mode
                changed_values.append("mode")

        if values.get("changed_by") is not None:
            self._values["changed_by"] = values["changed_by"]
            changed_values.append("changed_by")

        if values.get("set_user") is not None:
            self._values["set_user"] = values["set_user"]
            changed_values.append("set_user")

        if values.get("unset_user") is not None:
            self._values["unset_user"] = values["unset_user"]
            changed_values.append("unset_user")

        if values.get("pending_exit") is not None:
            self._values["pending_exit"] = values["pending_exit"]
            changed_values.append("pending_exit")

        return changed_values

    @property
    def alarm_status(self):
        _alarm_status = {
            "intrusion": False,
            "fire": False,
            "tamper": False,
            "problem": False,
            "verified": False,
        }

        for zone in self.zones:
            zone_alarm_status = zone.alarm_status
            for k in zone_alarm_status:
                if zone_alarm_status[k] is True:
                    _alarm_status[k] = True
                    if k == "intrusion" and _alarm_status[k] is True:
                        _alarm_status["verified"] = True
        return _alarm_status

    @property
    def intrusion(self) -> bool:
        return self.alarm_status.get("intrusion", False)

    @property
    def fire(self) -> bool:
        return self.alarm_status.get("fire", False)

    @property
    def tamper(self) -> bool:
        return self.alarm_status.get("tamper", False)

    @property
    def problem(self) -> bool:
        return self.alarm_status.get("problem", False)

    @property
    def verified(self) -> bool:
        return self.alarm_status.get("verified", False)

    async def async_command(self, command, code) -> int:
        if code is None:
            return SpcError(54).error

        username = None
        password = None
        username, password = self._bridge.get_user_credentials(code)
        if username is None or password is None:
            return SpcError(54).error

        if command == "clear_alerts":
            return await self._http_client.async_command_clear_alerts(
                username, password
            )
        else:
            err = await self._http_client.async_command_area(
                command, self._id, username, password
            )
            if command == "set_delayed" and err["code"] == 0:
                self._bridge.set_value("area", self._id, {"pending_exit": True})
            else:
                self._bridge.set_value("area", self._id, {"pending_exit": False})
            return err

    async def async_get_arm_status(self, arm_mode) -> dict:
        return await self._http_client.async_get_area_arm_status(arm_mode, self._id)
