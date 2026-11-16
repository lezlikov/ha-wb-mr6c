import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.modbus import async_get_temporary_unit
from modbus_connection import ModbusTcpParams

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_UNIT_ID,
    DEFAULT_PORT,
    DEFAULT_UNIT_ID,
)

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): int,
    }
)


class WBMR6CConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Обработка потока конфигурации для WB-MR6C v3."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                # Проверка подключения через временный unit
                async with async_get_temporary_unit(
                    self.hass,
                    ModbusTcpParams(
                        host=user_input[CONF_HOST],
                        port=user_input[CONF_PORT],
                    ),
                    user_input[CONF_UNIT_ID],
                ) as unit:
                    # Пробное чтение одного Coil-регистра (канал 1)
                    await unit.read_coil(0)
            except Exception:
                _LOGGER.exception("Не удалось подключиться к WB-MR6C")
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"WB-MR6C ({user_input[CONF_HOST]})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )