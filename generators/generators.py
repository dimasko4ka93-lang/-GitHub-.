from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> (
        Iterator)[Dict[str, Any]]:
    """Возвращает итератор транзакций в заданной валюте."""
    for tx in transactions:
        op_amount = tx.get("operationAmount")
        if not isinstance(op_amount, dict):
            continue

        currency_info = op_amount.get("currency")
        if not isinstance(currency_info, dict):
            continue

        if currency_info.get("code") == currency:
            yield tx


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Генератор, возвращает описание каждой транзакции по очереди."""
    for tx in transactions:
        desc = tx.get("description", "")
        yield str(desc) if desc is not None else ""


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генератор номеров карт в формате XXXX XXXX XXXX XXXX."""
    if start < 0 or end < 0:
        raise ValueError("Номера карт должны быть неотрицательными")
    if end - start > 1_000_000:
        raise ValueError("Слишком большой диапазон номеров карт")

    for number in range(start, end + 1):
        formatted = f"{number:016d}"

        yield f"{formatted[0:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:16]}"
