import logging
from datetime import timedelta

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from modbus_connection import ModbusError

from .const import DOMAIN, RELAY_COILS, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class WBMR6CCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, unit):
        super().__init__(
            hass,
            _LOGGER,
            name="wb_mr6c",
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self.unit = unit

    async def _async_update_data(self):
        try:
            return {
    channel: (await self.unit.read_coils(coil, 1))[0]
    for channel, coil in RELAY_COILS.items()
}
        except ModbusError as err:
            raise UpdateFailed(f"Ошибка чтения Modbus: {err}") from err


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    unit = hass.data[DOMAIN][entry.entry_id]
    coordinator = WBMR6CCoordinator(hass, unit)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        WBRelaySwitch(coordinator, channel) for channel in RELAY_COILS
    )


class WBRelaySwitch(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator: WBMR6CCoordinator, channel: int):
        super().__init__(coordinator)
        self._channel = channel
        self._attr_name = f"WB-MR6C Реле {channel}"
        self._attr_unique_id = f"wb_mr6c_relay_{channel}"
        self._attr_is_on = False

    @property
    def is_on(self):
        return self.coordinator.data.get(self._channel, False)

    async def async_turn_on(self, **kwargs):
        await self.coordinator.unit.write_coil(RELAY_COILS[self._channel], True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.unit.write_coil(RELAY_COILS[self._channel], False)
        await self.coordinator.async_request_refresh()