import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Ищет транзакции, в описании которых есть заданная строка.

    :param data: Список словарей с транзакциями
    :param search: Строка для поиска
    :return: Список словарей с найденными транзакциями
    """
    if not search:
        return []

    pattern = re.compile(search, re.IGNORECASE)
    result = []

    for transaction in data:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)

    return result
