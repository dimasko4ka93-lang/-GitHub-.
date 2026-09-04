# bank-masks
Модуль маскировки банковских карт: которая маскирует счета и банковские карты
## Возможности

- `get_mask_card_number(card: str) -> str` — маскирует номер карты (16 цифр) в формат `XXXX XX** **** XXXX`.
- `get_mask_account(account: str) -> str` — маскирует счёт, оставляя последние 4 цифры: `**XXXX`.
- `get_date(iso_datetime_str: str) -> str` — конвертирует ISO-дату с микросекундами в `ДД.ММ.ГГГГ`.
- `filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]` -Фильтрует список операций, возвращая только те, у которых поле state совпадает с указанным значением. По умолчанию выбираются операции со статусом "EXECUTED".
- `sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]` -Сортирует список операций по дате (по полю date в формате ISO).

