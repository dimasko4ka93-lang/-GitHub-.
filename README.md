# Bank Masks

Модуль маскировки банковских карт и счетов, а также обработки транзакций:
фильтрации, сортировки и генерации данных.

## Возможности

### Модуль `src/masks.py`: маскирование и форматирование

- `get_mask_card_number(card: str) -> str` — маскирует номер карты.
- `get_mask_account(account: str) -> str` — маскирует счёт.
- `get_date(iso_datetime_str: str) -> str` — конвертирует ISO-дату.

### Модуль `src/processing.py`: фильтрация и сортировка

- `filter_by_state(operations, state="EXECUTED") -> list[dict]` — фильтрует по статусу.
- `sort_by_date(operations, reverse=True) -> list[dict]` — сортирует по дате.

### Модуль `src/generators.py`: генераторы

- `filter_by_currency(transactions, currency) -> generator` — фильтрует по валюте.
- `transaction_descriptions(transactions) -> generator` — генерирует описания.
- `card_number_generator(start, stop) -> generator` — генерирует номера карт.

### Модуль `src/search.py`: поиск по описанию

- `process_bank_search(data: list[dict], search: str) -> list[dict]` — ищет транзакции по описанию с помощью `re`.

**Пример:**
```python
from src.search import process_bank_search

result = process_bank_search(data, "перевод")