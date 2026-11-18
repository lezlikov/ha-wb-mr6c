DOMAIN = "wb_mr6c"

CONF_SERIAL_PORT = "serial_port"
CONF_BAUDRATE = "baudrate"
CONF_UNIT_ID = "unit_id"

DEFAULT_BAUDRATE = 9600
DEFAULT_UNIT_ID = 151  # Изменено с 1 на 151 (ваш реальный адрес)

# Адреса Coil для каналов реле 1-6 (WB-MR6C v.3)
RELAY_COILS = {
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
}

SCAN_INTERVAL_SECONDS = 5
# Адреса регистров модели устройства (Input Registers)
DEVICE_MODEL_START = 200
DEVICE_MODEL_COUNT = 6