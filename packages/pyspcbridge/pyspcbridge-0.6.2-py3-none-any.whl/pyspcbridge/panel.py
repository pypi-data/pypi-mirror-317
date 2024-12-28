import logging

from .const import ArmMode
from .spc_error import SpcError

_LOGGER = logging.getLogger(__name__)


class Panel:
    """Represents a SPC panel."""

    def __init__(self, bridge, panel_data, areas):
        self._bridge = bridge
        self._id = panel_data.get("serial")
        self._type = panel_data.get("type")
        self._model = panel_data.get("model")
        self._serial = panel_data.get("serial")
        self._firmware = panel_data.get("firmware")
        self._pincode_length = int(panel_data.get("pincode_length", 0))
        self._http_client = bridge._http_client
        self._values = {
            "event": "",
            "changed_by": "",
        }
        self._areas = areas

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def model(self):
        return self._model

    @property
    def serial(self):
        return self._serial

    @property
    def firmware(self):
        return self._firmware

    @property
    def pincode_length(self):
        return self._pincode_length

    @property
    def a_enabled(self):
        for a in self._areas:
            if a.a_enabled:
                return a.a_enabled
        return False

    @property
    def a_name(self):
        for a in self._areas:
            if a.a_name is not None:
                return a.a_name
        return ""

    @property
    def b_enabled(self):
        for a in self._areas:
            if a.b_enabled:
                return a.b_enabled
        return False

    @property
    def b_name(self):
        for a in self._areas:
            if a.b_name is not None:
                return a.b_name
        return ""

    @property
    def exittime(self):
        _exittime = 0
        for a in self._areas:
            if a.exittime > _exittime:
                _exittime = a.exittime
        return _exittime

    @property
    def entrytime(self):
        _entrytime = 0
        for a in self._areas:
            if a.entrytime > _entrytime:
                _entrytime = a.entrytime
        return _entrytime

    @property
    def event(self) -> str:
        return self._values.get("event", "")

    @property
    def changed_by(self) -> str:
        return self._values.get("changed_by", "")

    @property
    def values(self):
        return self._values

    def change_values(self, values) -> list:
        changed_values = []
        if values.get("event") is not None:
            self._values["event"] = values["event"]
            changed_values.append("event")
        if values.get("changed_by") is not None:
            self._values["changed_by"] = values["changed_by"]
            changed_values.append("changed_by")
        return changed_values

    @property
    def mode(self):
        _mode = None
        for a in self._areas:
            _area_mode = a.mode
            if _mode is None:
                _mode = _area_mode
            elif _area_mode.value != _mode.value:
                _m = _mode
                if _area_mode.value > _mode.value:
                    _m = _area_mode
                if _m == ArmMode.PART_SET_A:
                    _mode = ArmMode.PARTLY_SET_A
                if _m == ArmMode.PART_SET_B:
                    _mode = ArmMode.PARTLY_SET_B
                if _m == ArmMode.FULL_SET:
                    _mode = ArmMode.PARTLY_FULL_SET

        return _mode

    @property
    def pending_exit(self):
        _state = False
        for a in self._areas:
            if a.pending_exit is True:
                _state = a.pending_exit
        return _state

    @property
    def alarm_status(self):
        _alarm_status = {
            "intrusion": False,
            "fire": False,
            "tamper": False,
            "problem": False,
            "verified": False,
        }

        for a in self._areas:
            _area_alarm_status = a.alarm_status
            for k in _area_alarm_status:
                if _area_alarm_status[k] is True:
                    _alarm_status[k] = True

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
        username = None
        password = None
        if code is not None:
            username, password = self._bridge.get_user_credentials(code)
            if username is None or password is None:
                return SpcError(54).error

        if command == "clear_alerts":
            return await self._http_client.async_command_clear_alerts(
                username, password
            )
        else:
            err = await self._http_client.async_command_area(
                command, None, username, password
            )
            if command == "set_delayed":
                if isinstance(err, dict) and err.get("code", 0) > 0:
                    return err
                if isinstance(err, list):
                    for e in err.values():
                        if e.get("code", 0) > 0:
                            return err
                for a in self._areas:
                    self._bridge.set_value("area", a.id, {"pending_exit": True})
            else:
                for a in self._areas:
                    self._bridge.set_value("area", a.id, {"pending_exit": False})
            return err

    async def async_get_arm_status(self, arm_mode) -> dict:
        return await self._http_client.async_get_area_arm_status(arm_mode)
