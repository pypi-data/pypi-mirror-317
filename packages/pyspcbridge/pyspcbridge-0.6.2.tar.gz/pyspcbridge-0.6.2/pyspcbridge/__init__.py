"""Python wrapper for the Lundix SPC Bridge REST API."""

import asyncio
import logging

from .area import Area
from .const import ZoneInput
from .door import Door
from .output import Output
from .panel import Panel
from .spc_http_client import SpcHttpClient
from .spc_ws_client import SpcWsClient
from .user import User
from .zone import Zone

_LOGGER = logging.getLogger(__name__)

__all__ = ["Area", "Door", "Output", "Panel", "User", "Zone", "ZoneInput"]


class SpcBridge:
    """Alarm system representation."""

    def __init__(
        self,
        gw_ip_address,
        gw_port,
        credentials,
        users_config,
        loop,
        session,
        http_client,
        async_callback,
    ):
        """Initialize the client."""
        self._async_callback = async_callback
        self._panel = None
        self._users = {}
        self._areas = {}
        self._zones = {}
        self._outputs = {}
        self._doors = {}
        self._users_config = users_config

        self._http_client = SpcHttpClient(
            gw_ip_address=gw_ip_address,
            gw_port=gw_port,
            credentials=credentials,
            http_client=http_client,
        )

        self._ws_client = SpcWsClient(
            bridge=self,
            gw_ip_address=gw_ip_address,
            gw_port=gw_port,
            credentials=credentials,
            loop=loop,
            session=session,
            http_client=self._http_client,
        )

    @property
    def info(self):
        """Retrieve basic panel info."""
        return self._info

    @property
    def panel(self):
        """Retrieve panel data."""
        return self._panel

    @property
    def users(self):
        """Retrieve all available users."""
        return self._users

    @property
    def areas(self):
        """Retrieve all available areas."""
        return self._areas

    @property
    def zones(self):
        """Retrieve all available zones."""
        return self._zones

    @property
    def outputs(self):
        """Retrieve all available outputs (mapping gates)."""
        return self._outputs

    @property
    def doors(self):
        """Retrieve all available doors."""
        return self._doors

    def ws_start(self):
        """Start Websocket communication"""
        self._ws_client.ws_start()

    def ws_stop(self):
        """Stop Websocket communication"""
        self._ws_client.ws_stop()

    def set_value(self, resource, id, values):
        if resource == "panel":
            if self._panel.change_values(values):
                asyncio.create_task(
                    self._async_callback("update", self._panel.id, [self._panel])
                )

        if resource == "area":
            area = self._areas[id]
            if area:
                if area.change_values(values):
                    asyncio.create_task(
                        self._async_callback(
                            "update", self._panel.id, [area, self._panel]
                        )
                    )

        if resource == "zone":
            zone = self._zones[id]
            if zone:
                changed_values = zone.change_values(values)
                if "input" in changed_values and "status" not in changed_values:
                    # Only zone is needed to update
                    asyncio.create_task(
                        self._async_callback("update", self._panel.id, [zone])
                    )
                elif changed_values:
                    # Update zone, area of zone and panel
                    asyncio.create_task(
                        self._async_callback(
                            "update", self._panel.id, [zone, zone._area, self._panel]
                        )
                    )

        if resource == "output":
            output = self._outputs[id]
            if output:
                if output.change_values(values):
                    asyncio.create_task(
                        self._async_callback("update", self._panel.id, [output])
                    )

        if resource == "door":
            door = self._doors[id]
            if door:
                if door.change_values(values):
                    asyncio.create_task(
                        self._async_callback("update", self._panel.id, [door])
                    )

    def get_user_credentials(self, code):
        """Parse a user code and return user's name and password"""
        if self._users_config:
            for u in self._users.values():
                if code == u.ha_pincode:
                    return u.name, u.spc_password
        else:
            spc_len = self._panel.pincode_length
            code_len = len(code)
            if code_len > spc_len:
                userid = code[: (code_len - spc_len)]
                if u := self._users.get(int(userid)):
                    return u.name, code[-spc_len:]
        return None, None

    async def async_load_config(self):
        """Fetch configuration from SPC to initialize."""

        _LOGGER.debug("Load SPC configuration")
        try:
            panel_data = await self._http_client.async_get_panel()
            await asyncio.sleep(0.1)
            users_data = await self._http_client.async_get_users()
            await asyncio.sleep(0.1)
            areas_data = await self._http_client.async_get_areas()
            await asyncio.sleep(0.1)
            zones_data = await self._http_client.async_get_zones()
            await asyncio.sleep(0.1)
            outputs_data = await self._http_client.async_get_outputs()
            await asyncio.sleep(0.1)
            doors_data = await self._http_client.async_get_doors()

            # Get exit and entry times for each area
            for a in areas_data:
                a["exittime"] = 0
                a["entrytime"] = 0
                if (id := a.get("id")) is not None:
                    await asyncio.sleep(0.1)
                    config = await self._http_client.async_get_area_configs(id=id)
                    if config and list(config):
                        a["exittime"] = config[0].get("exittime", 0)
                        a["entrytime"] = config[0].get("entrytime", 0)

        except Exception as err:
            _LOGGER.warning("Exception trying to get SPC data: %s", err)
            raise

        if not zones_data or not areas_data:
            return False

        """ Create class objects """
        for a in areas_data:
            area = Area(self, a)
            area_zones = [
                Zone(self, area, z)
                for z in zones_data
                if z.get("area_id") == a.get("id")
            ]
            area.zones = area_zones
            self._areas[area.id] = area
            self._zones.update({z.id: z for z in area_zones})

        self._panel = Panel(self, panel_data, self._areas.values())

        for u in users_data:
            user = User(u, self._users_config)
            self._users[user.id] = user

        for o in outputs_data:
            output = Output(self, o)
            self._outputs[output.id] = output

        for d in doors_data:
            door = Door(self, d)
            self._doors[door.id] = door

        return True

    async def async_reload_config(self):
        """Reload configuration from SPC."""
        _LOGGER.debug("Reload SPC configuration")
        asyncio.create_task(self._async_callback("reload", self._panel.id))
        return True

    async def test_connection(self):
        """Test that communication parameters are valid"""
        try:
            panel_data = await self._http_client.async_get_panel()
            await asyncio.sleep(0.1)
            users_data = await self._http_client.async_get_users()
            await asyncio.sleep(0.1)
            areas_data = await self._http_client.async_get_areas()
            await asyncio.sleep(0.1)
            zones_data = await self._http_client.async_get_zones()
            await asyncio.sleep(0.1)
            outputs_data = await self._http_client.async_get_outputs()
            await asyncio.sleep(0.1)
            doors_data = await self._http_client.async_get_doors()
            await asyncio.sleep(0.1)

            spc_data = {
                "panel": panel_data,
                "users": users_data,
                "areas": areas_data,
                "zones": zones_data,
                "outputs": outputs_data,
                "doors": doors_data,
            }

            self.ws_start()
            for _ in range(10):
                await asyncio.sleep(1)
                if self._ws_client.ws_state() == "running":
                    self.ws_stop()
                    return spc_data

            self.ws_stop()
            return None
        except Exception:
            self.ws_stop()
            return None

    async def async_command(self, command, id) -> int:
        try:
            if command == "clear_alerts":
                return await self._http_client.async_command_clear_alerts()
            else:
                return await self._http_client.async_command_area(command, id)
        except Exception:
            raise

    async def async_get_arm_status(self, arm_mode, id=None) -> dict:
        try:
            return await self._http_client.async_get_area_arm_status(arm_mode, id)
        except Exception:
            raise
