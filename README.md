# Bank Masks

Модуль маскировки банковских карт и счетов, а также обработки транзакций:
фильтрации, сортировки и генерации данных.

## Возможности

### Модуль src/masks.py: маскирование и форматирование

- `get_mask_card_number(card: str) -> str` — маскирует номер карты (16 цифр) в формат `XXXX XX** **** XXXX`.
- `get_mask_account(account: str) -> str` — маскирует счёт, оставляя последние 4 цифры: `**XXXX`.
- `get_date(iso_datetime_str: str) -> str` — конвертирует ISO-дату с микросекундами в формат `ДД.ММ.ГГГГ`.

### Модуль src/processing.py: фильтрация и сортировка операций

- `filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]` — фильтрует список операций.
- `sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]` — сортирует список операций по дате.

### Модуль src/generators.py: работа с большими объёмами данных

- `filter_by_currency(transactions: list[dict], currency: str) -> generator` — фильтрует по валюте.
- `transaction_descriptions(transactions: list[dict]) -> generator` — генерирует описания.
- `card_number_generator(start: int, stop: int) -> generator` — генерирует номера карт.

## Чтение JSON-файла

Модуль `src/utils.py` содержит функцию `load_operations`.

### Что делает
- Принимает путь к JSON-файлу с транзакциями
- Возвращает список словарей
- Если файл пустой, не список или не найден → возвращает `[]`

### Использование
```python
from src.utils import load_operations

operations = load_operations("data/operations.json")
