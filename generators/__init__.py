def filter_by_currency(transactions, currency):
    """Генератор: фильтрует транзакции по валюте."""
    for t in transactions:
        if not isinstance(t, dict):
            continue
        op_amount = t.get("operationAmount")
        if not isinstance(op_amount, dict):
            continue
        cur = op_amount.get("currency")
        if not isinstance(cur, dict):
            continue
        if cur.get("code") == currency:
            yield t


def transaction_descriptions(transactions=None):
    """Генератор: возвращает описания транзакций (пустая строка если нет)."""
    if transactions is None:
        transactions = []
    for t in transactions:
        if isinstance(t, dict):
            yield t.get("description") or ""
        else:
            yield ""


def card_number_generator(start, end):
    """Генератор: выдаёт номера карт от start до end включительно,
    отформатированные как XXXX XXXX XXXX XXXX."""
    if start < 0 or end < 0:
        raise ValueError("Номер карты не может быть отрицательным")
    if end - start > 1_000_000:
        raise ValueError("Диапазон слишком большой")
    for num in range(start, end + 1):
        formatted = f"{num:016d}"
        yield " ".join(formatted[i:i + 4] for i in range(0, 16, 4))