import logging

_LOGGER = logging.getLogger(__name__)


class User:
    """Represents a SPC user."""

    def __init__(self, spc_user, users_config):
        self._id = spc_user.get("id")
        self._name = spc_user.get("name")
        if users_config and users_config.get(str(self._id)):
            self._ha_pincode = users_config[str(self._id)].get("ha_pincode", "")
            self._spc_password = users_config[str(self._id)].get("spc_password", "")
        else:
            self._ha_pincode = ""
            self._spc_password = ""

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def ha_pincode(self):
        return self._ha_pincode

    @property
    def spc_password(self):
        return self._spc_password
