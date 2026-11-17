import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from modbus_connection import ModbusError

from .const import DOMAIN, CONF_UNIT_ID

_LOGGER = logging.getLogger(__name__)

FW_VERSION_START = 250
FW_VERSION_COUNT = 16


class WBMR6CFirmwareCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, unit, slave_id: int):
        super().__init__(
            hass,
            _LOGGER,
            name="wb_mr6c_firmware",
            update_interval=timedelta(hours=1),
        )
        self.unit = unit
        self.slave_id = slave_id

    async def _async_update_data(self):
        try:
            registers = await self.unit.read_input_registers(
                FW_VERSION_START, FW_VERSION_COUNT
            )
            # Берем младший байт из каждого регистра и декодируем
            raw_bytes = bytes([reg & 0xFF for reg in registers if reg != 0])
            version = raw_bytes.decode("ascii", errors="ignore")
            return version
        except ModbusError as err:
            raise UpdateFailed(f"Ошибка чтения версии прошивки: {err}") from err


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    unit = hass.data[DOMAIN][entry.entry_id]
    slave_id = entry.data[CONF_UNIT_ID]

    coordinator = WBMR6CFirmwareCoordinator(hass, unit, slave_id)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([WBFirmwareSensor(coordinator)])


class WBFirmwareSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: WBMR6CFirmwareCoordinator):
        super().__init__(coordinator)
        self._attr_name = "Версия прошивки"
        self._attr_unique_id = f"wb_mr6c_fw_{coordinator.slave_id}"
        self._attr_icon = "mdi:chip"

    @property
    def native_value(self):
        return self.coordinator.data

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, f"wb_mr6c_{self.coordinator.slave_id}")},
        )