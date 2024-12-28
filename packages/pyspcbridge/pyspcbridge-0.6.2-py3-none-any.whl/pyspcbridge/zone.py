import logging

from .const import ZoneInput, ZoneStatus, ZoneType
from .spc_error import SpcError
from .utils import _load_enum

_LOGGER = logging.getLogger(__name__)


class Zone:
    """Represents a SPC zone."""

    def __init__(self, bridge, area, zone_data):
        self._bridge = bridge
        self._id = zone_data.get("id")
        self._name = zone_data.get("name")
        self._area = area
        self._http_client = bridge._http_client
        self._type = _load_enum(ZoneType, zone_data.get("type", 0))
        self._values = {
            "input": _load_enum(ZoneInput, zone_data.get("input", 0)),
            "status": _load_enum(ZoneStatus, zone_data.get("status", 0)),
        }

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return self._values

    def change_values(self, values) -> list:
        changed_values = []

        if values.get("input") is not None:
            new_input = _load_enum(ZoneInput, values["input"])
            if new_input != self._values["input"]:
                self._values["input"] = new_input
                changed_values.append("input")

        if values.get("status") is not None:
            new_status = _load_enum(ZoneStatus, values["status"])
            if new_status != self._values["status"]:
                self._values["status"] = new_status
                changed_values.append("status")

        return changed_values

    @property
    def state(self) -> bool:
        return self._values["input"] == ZoneInput.OPEN

    @property
    def input(self):
        return self._values["input"]

    @property
    def alarm_status(self):
        _alarm_status = {
            "intrusion": False,
            "fire": False,
            "tamper": False,
            "problem": False,
        }
        zone_input = self._values["input"]
        zone_status = self._values["status"]
        zone_type = self._type

        if zone_status == ZoneStatus.TAMPER:
            _alarm_status["tamper"] = True
        elif zone_status == ZoneStatus.ALARM:
            if (
                zone_type == ZoneType.ALARM
                or zone_type == ZoneType.ENTRY_EXIT
                or zone_type == ZoneType.GLASSBREAK
                or zone_type == ZoneType.ENTRY_EXIT_2
            ):
                _alarm_status["intrusion"] = True
            elif zone_type == ZoneType.FIRE:
                _alarm_status["fire"] = True
            elif zone_type == ZoneType.TAMPER:
                _alarm_status["tamper"] = True

        if zone_input != ZoneInput.CLOSED and zone_input != ZoneInput.OPEN:
            _alarm_status["problem"] = True

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
    def inhibited(self) -> bool:
        return self._values["status"] == ZoneStatus.INHIBIT

    @property
    def isolated(self) -> bool:
        return self._values["status"] == ZoneStatus.ISOLATE

    async def async_command(self, command, code) -> dict:
        if code is None:
            return SpcError(54).error

        username = None
        password = None
        username, password = self._bridge.get_user_credentials(code)
        if username is None or password is None:
            return SpcError(54).error

        return await self._http_client.async_command_zone(
            command, self._id, username, password
        )
