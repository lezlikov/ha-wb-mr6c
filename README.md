# WB-MR6C v3 для Home Assistant

Кастомная интеграция для реле Wiren Board WB-MR6C v.3 через Modbus TCP.

## Требования
- Home Assistant 2026.10+
- WB-MR6C v.3, подключённый через Modbus TCP (шлюз или преобразователь)

## Установка
1. Скопируйте папку `custom_components/wb_mr6c` в `/config/custom_components/`
2. Перезапустите Home Assistant
3. Настройки → Устройства и службы → Добавить интеграцию → WB-MR6C v3
4. Укажите IP, порт и Modbus-адрес устройства

## Регистры
Каналы 1–6: Coil 0–5 [citation:16]