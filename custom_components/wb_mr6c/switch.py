from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.switch import SwitchEntity
# ... другие импорты ...

class WBRelaySwitch(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator: WBMR6CCoordinator, channel: int):
        super().__init__(coordinator)
        self._channel = channel
        self._attr_name = f"WB-MR6C Реле {channel}"
        self._attr_unique_id = f"wb_mr6c_relay_{channel}"
        self._attr_is_on = False

    @property
    def device_info(self) -> DeviceInfo:
        # self.coordinator.unit.slave — это Modbus-адрес, который вы указали (151, 152 и т.д.)
        # Если атрибут называется иначе, проверьте в объекте unit
        slave_id = getattr(self.coordinator.unit, 'slave', 'unknown') 
        return DeviceInfo(
            identifiers={(DOMAIN, f"wb_mr6c_{slave_id}")},
            name=f"WB-MR6C (ID: {slave_id})",
            manufacturer="Wiren Board",
            model="WB-MR6C v.3",
        )

    @property
    def is_on(self):
        return self.coordinator.data.get(self._channel, False)

    async def async_turn_on(self, **kwargs):
        await self.coordinator.unit.write_coil(RELAY_COILS[self._channel], True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.unit.write_coil(RELAY_COILS[self._channel], False)
        await self.coordinator.async_request_refresh()