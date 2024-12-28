"""SPC http client"""

import logging

import httpx

from .exceptions import RequestError, raise_error
from .spc_error import SpcError

_LOGGER = logging.getLogger(__name__)


class SpcHttpClient:
    def __init__(self, gw_ip_address, gw_port, credentials, http_client):
        self._gw_ip_address = gw_ip_address
        self._gw_port = gw_port
        self._credentials = credentials
        self._http_client = http_client

    async def _async_request(self, http_client, _auth, url):
        try:
            if _auth:
                response = await http_client(
                    url,
                    auth=_auth,
                    timeout=5,
                )
            else:
                response = await http_client(
                    url,
                    timeout=5,
                )

            if response.status_code != 200 and response.status_code != 404:
                _LOGGER.error(
                    "Error getting/settings SPC data from/to %s, HTTP status %d",
                    url,
                    response.status_code,
                )
                raise_error(response.status_code)

            result = response.json()

        except httpx.TimeoutException as errt:
            message = f"Timeout getting/setting SPC data from/to {url}."
            _LOGGER.error(message)
            raise RequestError(message) from errt

        except (httpx.TransportError, httpx.HTTPStatusError) as errc:
            message = f"Error getting/setting SPC data from/to {url}."
            _LOGGER.error(message)
            raise RequestError(message) from errc

        except httpx.RequestError as err:
            message = f"Error getting/setting SPC data from/to {url}."
            _LOGGER.error(message)
            raise RequestError(message) from err

        return result

    async def _async_get_data(self, resource, id=None):
        """Get the SPC data for the resource. (HTTP GET)"""
        proto = "http"
        auth = None
        if len(self._credentials["get_username"]) and len(
            self._credentials["get_password"]
        ):
            proto = "https"
            auth = httpx.DigestAuth(
                username=self._credentials["get_username"],
                password=self._credentials["get_password"],
            )

        if id is not None:
            url = f"{proto}://{self._gw_ip_address}:{self._gw_port}/spc/{resource}/{id}"
        else:
            url = f"{proto}://{self._gw_ip_address}:{self._gw_port}/spc/{resource}"

        try:
            data = await self._async_request(self._http_client.get, auth, url)
            if not data:
                _LOGGER.error("Unable to get data from SPC")
                return None
        except Exception:
            _LOGGER.error("Unable to get data from SPC")
            raise

        return data

    async def _async_put_data(
        self, resource, command, id=None, username=None, password=None
    ):
        """Send a command to SPC (HTTP PUT)."""
        proto = "http"
        auth = None
        if len(self._credentials["put_username"]) and len(
            self._credentials["put_password"]
        ):
            proto = "https"
            auth = httpx.DigestAuth(
                username=self._credentials["put_username"],
                password=self._credentials["put_password"],
            )

        if id is not None:
            url = f"{proto}://{self._gw_ip_address}:{self._gw_port}/spc/{resource}/{id}/{command}"
        else:
            url = f"{proto}://{self._gw_ip_address}:{self._gw_port}/spc/{resource}/{command}"

        if username and password:
            url = f"{url}?username={username}&password={password}"

        try:
            data = await self._async_request(self._http_client.put, auth, url)
            if not data:
                _LOGGER.error("Unable to send a command to SPC")
                return None
        except Exception:
            _LOGGER.error("Unable to to send a command to SPC")
            raise

        return data

    def _validate_header(self, reply) -> int:
        if (
            not reply
            or (
                reply.get("status", "") != "success"
                and reply.get("status", "") != "error"
            )
            or not reply.get("data")
        ):
            return 998
        if (err := int(reply["data"].get("code", -1))) > 0:
            return err
        if reply.get("status", "") == "error":
            return 998
        return 0

    async def async_get_users(self, id=None):
        """Get Users data"""

        def _normalize(d):
            return {
                "id": int(d.get("user_id", 0)),
                "name": d.get("name", ""),
            }

        data = await self._async_get_data("user", id)
        if data and data.get("status", "") == "success" and data.get("data"):
            users = data["data"].get("user_config")
            if isinstance(users, dict):
                return [_normalize(u) for u in [users]]
            elif isinstance(users, list):
                return [_normalize(u) for u in users]
        return {}

    async def async_get_panel(self):
        """Get Panel data"""
        data = await self._async_get_data("panel")
        if data and data.get("status", "") == "success" and data.get("data"):
            panel = data["data"].get("panel_summary")
            if panel:
                return {
                    "type": panel.get("spc_type", ""),
                    "model": panel.get("spc_variant", ""),
                    "serial": panel.get("spc_serial_no", ""),
                    "firmware": panel.get("spc_fw_version", ""),
                    "pincode_length": panel.get("pin_digits", 4),
                }
            else:
                return None

    async def async_get_area_configs(self, id=None):
        """Get Area config"""

        def _normalize(a):
            return {
                "id": int(a.get("id", 0)),
                "entrytime": int(a.get("entrytime", 0)),
                "exittime": int(a.get("exittime", 0)),
            }

        if id is not None:
            data = await self._async_get_data(f"area/{id}/config")
        else:
            data = await self._async_get_data("area/config")

        if data and data.get("status", "") == "success" and data.get("data"):
            areas = data["data"].get("area")
            if isinstance(areas, dict):
                return [_normalize(a) for a in [areas]]
            elif isinstance(areas, list):
                return [_normalize(a) for a in areas]

        return {}

    async def async_get_area_arm_status(self, arm_mode, id=None):
        """Get Area arm status"""

        def _normalize(a):
            reasons = []
            for x in range(100):
                if (reason := a.get(f"reason_{x}")) is not None:
                    r = int(reason)
                    if r > 100 and r < 999:
                        reasons.append(f"area_{r-100}")
                    elif r > 1000 and r < 1999:
                        reasons.append(f"zone_{r-1000}")
                    elif r == 10006:
                        reasons.append("engineer_on_site")
                    elif r == 10007:
                        reasons.append("no_rights")
                    elif r != 0:
                        reasons.append("undefined")
                else:
                    break
            return {
                "area_id": int(a.get("area_id", 0)),
                "reasons": reasons,
            }

        if id is not None:
            data = await self._async_get_data(f"area/{id}/{arm_mode}_status")
        else:
            data = await self._async_get_data(f"area/{arm_mode}_status")

        if (
            data
            and data.get("status", "") == "success"
            and data.get("data")
            and (d := data.get("data").get("reply_get_area_change_mode_status"))
        ):
            areas = d.get("area_change_mode_status")
            if isinstance(areas, dict):
                return [_normalize(a) for a in [areas]]
            elif isinstance(areas, list):
                return [_normalize(a) for a in areas]
        return {}

    async def async_get_areas(self, id=None):
        """Get Area data"""

        def _normalize(a):
            return {
                "id": int(a.get("area_id", 0)),
                "name": a.get("area_name", ""),
                "mode": int(a.get("mode", 0)),
                "a_enabled": int(a.get("partseta_enable", 0)) == 1,
                "a_name": a.get("partseta_name", "") or "",
                "b_enabled": int(a.get("partsetb_enable", 0)) == 1,
                "b_name": a.get("partsetb_name", ""),
                "set_user": a.get("last_set_user_name", ""),
                "unset_user": a.get("last_unset_user_name", ""),
            }

        data = await self._async_get_data("area", id)
        if data and data.get("status", "") == "success" and data.get("data"):
            areas = data["data"].get("area_status")
            if isinstance(areas, dict):
                return [_normalize(a) for a in [areas]]
            elif isinstance(areas, list):
                return [_normalize(a) for a in areas]
        return {}

    async def async_get_zones(self, id=None):
        """Get Zone data"""

        def _normalize(z):
            return {
                "id": int(z.get("zone_id", 0)),
                "name": z.get("zone_name", ""),
                "type": int(z.get("type", 0)),
                "input": int(z.get("input", 0)),
                "status": int(z.get("status", 0)),
                "area_id": int(z.get("area_id", 0)),
                "area_name": z.get("area_name", ""),
            }

        data = await self._async_get_data("zone", id)
        if data and data.get("status", "") == "success" and data.get("data"):
            zones = data["data"].get("zone_status")
            if isinstance(zones, dict):
                return [_normalize(z) for z in [zones]]
            elif isinstance(zones, list):
                return [_normalize(z) for z in zones]
        return {}

    async def async_get_outputs(self, id=None):
        """Get Output data"""

        def _normalize(o):
            return {
                "id": int(o.get("mg_id", 0)),
                "name": o.get("mg_name", ""),
                "state": int(o.get("state", 0)),
            }

        data = await self._async_get_data("output", id)
        if data and data.get("status", "") == "success" and data.get("data"):
            outputs = data["data"].get("mg_status")
            if isinstance(outputs, dict):
                return [_normalize(o) for o in [outputs]]
            elif isinstance(outputs, list):
                return [_normalize(o) for o in outputs]
        return {}

    async def async_get_doors(self, id=None):
        """Get Door data"""

        def _normalize(d):
            return {
                "id": int(d.get("door_id", 0)),
                "name": d.get("zone_name", ""),
                "status": int(d.get("status", 0)),
                "mode": int(d.get("mode", 0)),
            }

        data = await self._async_get_data("door", id)
        if data and data.get("status", "") == "success" and data.get("data"):
            doors = data["data"].get("door_status")
            if isinstance(doors, dict):
                return [_normalize(d) for d in [doors]]
            elif isinstance(doors, list):
                return [_normalize(d) for d in doors]
        return {}

    async def async_command_area(
        self, command, id=None, username=None, password=None
    ) -> dict:
        """Area commands"""
        try:
            reply = await self._async_put_data("area", command, id, username, password)
            if (err := self._validate_header(reply)) > 0:
                return SpcError(err).error

            _data = reply.get("data")
            if (
                _data.get("reply_area_change_mode")
                and (err := int(_data.get("reply_area_change_mode").get("result", -1)))
                > 0
            ):
                return SpcError(err).error
            if _area_change_mode := _data.get("reply_area_change_mode").get(
                "area_change_mode"
            ):
                if isinstance(_area_change_mode, dict):
                    if (err := int(_area_change_mode.get("result", -1))) >= 0:
                        return SpcError(err).error
                elif isinstance(_area_change_mode, list):
                    errors = {}
                    for a in _area_change_mode:
                        if (id := int(a.get("area_id", -1)) > 0) and (
                            err := int(a.get("result", -1)) >= 0
                        ):
                            errors[id] = SpcError(err).error
                        else:
                            return SpcError(998).error
                    return errors

            return SpcError(998).error
        except Exception as err:
            return SpcError(998).error

    async def async_command_zone(
        self, command, id=None, username=None, password=None
    ) -> dict:
        """Zone commands"""
        try:
            reply = await self._async_put_data("zone", command, id, username, password)
            if (err := self._validate_header(reply)) > 0:
                return SpcError(err).error

            _data = reply.get("data")
            if (
                _data.get("reply_zone_control")
                and (err := int(_data.get("reply_zone_control").get("result", -1))) > 0
            ):
                return SpcError(err).error
            if (
                _data.get("reply_zone_control").get("zone_control")
                and (
                    err := int(
                        _data.get("reply_zone_control")
                        .get("zone_control")
                        .get("result", -1)
                    )
                )
                >= 0
            ):
                return SpcError(err).error
            else:
                return SpcError(998).error
        except Exception as err:
            return SpcError(998).error

    async def async_command_output(
        self, command, id=None, username=None, password=None
    ):
        """Output commands"""
        try:
            reply = await self._async_put_data(
                "output", command, id, username, password
            )
            if (err := self._validate_header(reply)) > 0:
                return SpcError(err).error

            _data = reply.get("data")
            if (
                _data.get("reply_mg_control")
                and (err := int(_data.get("reply_mg_control").get("result", -1))) > 0
            ):
                return SpcError(err).error
            if (
                _data.get("reply_mg_control").get("mg_control")
                and (
                    err := int(
                        _data.get("reply_mg_control")
                        .get("mg_control")
                        .get("result", -1)
                    )
                )
                >= 0
            ):
                return SpcError(err).error
            else:
                return SpcError(998).error
        except Exception as err:
            return SpcError(998).error

    async def async_command_door(self, command, id=None, username=None, password=None):
        """Door commands"""
        try:
            reply = await self._async_put_data("door", command, id, username, password)
            if (err := self._validate_header(reply)) > 0:
                return SpcError(err).error

            _data = reply.get("data")
            if (
                _data.get("reply_door_control")
                and (err := int(_data.get("reply_door_control").get("result", -1))) > 0
            ):
                return SpcError(err).error
            if (
                _data.get("reply_door_control").get("door_control_result")
                and (
                    err := int(
                        _data.get("reply_door_control")
                        .get("door_control_result")
                        .get("result", -1)
                    )
                )
                >= 0
            ):
                return SpcError(err).error
            else:
                return SpcError(998).error
        except Exception as err:
            return SpcError(998).error

    async def async_command_clear_alerts(self, username=None, password=None):
        """Command - Clear All Alerts"""
        try:
            reply = await self._async_put_data(
                "alert", "clear", username=username, password=password
            )
            if (err := self._validate_header(reply)) > 0:
                return SpcError(err).error

            _data = reply.get("data")
            if (
                _data.get("reply_clear_all_alerts")
                and (err := int(_data.get("reply_clear_all_alerts").get("result", -1)))
                >= 0
            ):
                return SpcError(err).error
            else:
                return SpcError(998).error
        except Exception as err:
            return SpcError(998).error
