import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.modbus import async_get_unit
from modbus_connection import ModbusTcpParams

from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_UNIT_ID

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Настройка интеграции из config entry."""
    unit = async_get_unit(
        hass,
        entry,
        ModbusTcpParams(
            host=entry.data[CONF_HOST],
            port=entry.data[CONF_PORT],
        ),
        entry.data[CONF_UNIT_ID],
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = unit

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Выгрузка интеграции."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok