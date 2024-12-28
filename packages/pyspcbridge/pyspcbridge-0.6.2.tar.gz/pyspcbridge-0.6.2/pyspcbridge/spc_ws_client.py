"""SPC Websocket client"""

import json
import logging

from .websocket import AIOWSClient

_LOGGER = logging.getLogger(__name__)


class SpcWsClient:
    """SPC Websocket Client Class"""

    def __init__(
        self, bridge, gw_ip_address, gw_port, credentials, loop, session, http_client
    ):
        """Initialize the client."""
        self._bridge = bridge
        self._gw_ip_address = gw_ip_address
        self._gw_port = gw_port
        self._credentials = credentials
        self._loop = loop
        self._session = session
        self._set_value = bridge.set_value
        self._http_client = http_client
        self._websocket = None

    def ws_start(self):
        """Connect websocket to SPC Web Gateway."""
        _LOGGER.debug(
            "Start websocket communication with SPC Bridge: %s:%i",
            self._gw_ip_address,
            self._gw_port,
        )
        proto = "ws"
        params = ""
        if len(self._credentials["ws_username"]) and len(
            self._credentials["ws_password"]
        ):
            proto = "wss"
            params = f"?username={self._credentials["ws_username"]}&password={self._credentials["ws_password"]}&flexc_poll_events=1"

        url = f"{proto}://{self._gw_ip_address}:{self._gw_port}/ws/spc{params}"
        self._websocket = AIOWSClient(
            loop=self._loop,
            session=self._session,
            url=url,
            async_callback=self._async_ws_handler,
        )
        self._websocket.start()

    def ws_stop(self):
        """Disconnect websocket to SPC Web Gateway."""
        _LOGGER.debug(
            "Stop websocket communication with SPC Bridge: %s:%i",
            self._gw_ip_address,
            self._gw_port,
        )
        if self._websocket:
            self._websocket.stop()
        self._websocket = None

    def ws_state(self):
        if self._websocket:
            return self._websocket.state

    def _handle_output_event(self, event):
        output_id = int(event.get("mg_id", 0))
        event_id = int(event.get("ev_id", 0))
        state = None
        if event_id == 7013:
            state = True
        elif event_id == 7014:
            state = False

        if state is not None and output_id > 0:
            return self._set_value("output", output_id, {"state": state})
        return False

    def _handle_door_event(self, event):
        door_id = int(event.get("door_id", 0))
        event_id = int(event.get("ev_id", 0))
        username = event.get("user_name", "")

        if event_id == 3000:
            return self._set_value("door", door_id, {"entry_granted_user": username})

        if event_id == 3001:
            return self._set_value("door", door_id, {"entry_denied_user": username})
            return
        if event_id == 3002:
            return self._set_value("door", door_id, {"exit_granted_user": username})

        if event_id == 3003:
            return self._set_value("door", door_id, {"exit_denied_user": username})
            return

        mode = None
        if event_id == 3007:  # Normal mode
            mode = 0
        elif event_id == 3008:  # Locked mode
            mode = 1
        elif event_id == 3009:  # Unlocked mode
            mode = 2

        if mode is not None and door_id > 0:
            return self._set_value("door", door_id, {"mode": mode})
        return False

    async def _handle_system_event(self, event):
        # Reload and Update all SPC data after Engineer logout
        await self._bridge.async_reload_config()
        return

    def _handle_area_event(self, event):
        event_id = int(event.get("ev_id", 0))
        area_id = int(event.get("area_id", 0))
        sia_code = event.get("sia_code", "")
        username = event.get("user_name", "")

        if area_id > 0:
            if sia_code == "OG":  # Unset
                # Arm mode 0 and disarm username
                self._set_value(
                    "area",
                    area_id,
                    {
                        "mode": 0,
                        "unset_user": username,
                        "changed_by": username,
                        "pending_exit": False,
                    },
                )
                self._set_value("panel", None, {"changed_by": username})
                return
            elif sia_code == "NL":
                if event_id == 3502:  # Partset A
                    self._set_value(
                        "area",
                        area_id,
                        {"mode": 1, "changed_by": username, "pending_exit": False},
                    )
                    self._set_value("panel", None, {"changed_by": username})
                    return
                elif event_id == 3503:  # Partset B
                    self._set_value(
                        "area",
                        area_id,
                        {"mode": 2, "changed_by": username, "pending_exit": False},
                    )
                    self._set_value("panel", None, {"changed_by": username})
                    return
            elif sia_code == "CG":  # Fullset
                self._set_value(
                    "area",
                    area_id,
                    {
                        "mode": 3,
                        "set_user": username,
                        "changed_by": username,
                        "pending_exit": False,
                    },
                )
                self._set_value("panel", None, {"changed_by": username})
                return

        return

    async def _async_handle_zone_event(self, event):
        event_id = int(event.get("ev_id", 0))
        zone_id = int(event.get("zone_id", 0))

        if (
            (event_id >= 1000 and event_id <= 1029)
            or (event_id >= 1100 and event_id <= 1129)
            or (event_id >= 1200 and event_id <= 1223)
            or (event_id >= 1300 and event_id <= 1323)
            or (event_id >= 1400 and event_id <= 1423)
            or (event_id >= 1500 and event_id <= 1523)
            or (event_id >= 1600 and event_id <= 1623)
            or (event_id >= 1700 and event_id <= 1723)
            or (event_id >= 1800 and event_id <= 1823)
            or (event_id >= 1900 and event_id <= 1923)
            or (event_id >= 2000 and event_id <= 2023)
            or (event_id >= 2100 and event_id <= 2117)
            or (event_id >= 8004 and event_id <= 8005)
        ):
            if zone_id > 0:
                try:
                    data = await self._http_client.async_get_zones(id=zone_id)
                    if data and isinstance(data, list):
                        zone = data[0]
                        id = zone.get("id", 0)
                        input = zone.get("input", 0)
                        status = zone.get("status", 0)
                        if id > 0:
                            self._set_value(
                                "zone", id, {"input": input, "status": status}
                            )
                            return True

                    return False

                except Exception as err:
                    _LOGGER.warning("SPC EXCEPTION: %s", err)
                    return False

    async def _async_ws_handler(self, data):
        """Process incoming websocket message."""
        event = data["data"].get("sia") or data["data"].get("event")
        if event is None:
            return

        self._set_value("panel", None, {"event": json.dumps(event)})

        event_id = int(event.get("ev_id", 0))
        sia_code = event.get("sia_code", "")

        # Output events
        if event_id == 7013 or event_id == 7014:
            self._handle_output_event(event)
            return

        # Door events
        if (
            event_id == 3000
            or event_id == 3001
            or event_id == 3002
            or event_id == 3003
            or event_id == 3007
            or event_id == 3008
            or event_id == 3009
        ):
            self._handle_door_event(event)
            return

        # System events
        if sia_code == "LX":
            await self._handle_system_event(event)
            return

        # Area events
        if sia_code == "CI" or sia_code == "CG" or sia_code == "OG" or sia_code == "NL":
            self._handle_area_event(event)
            return

        # Zone events
        await self._async_handle_zone_event(event)
        return
