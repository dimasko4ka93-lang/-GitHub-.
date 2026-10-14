from collections import Counter


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Считает количество операций в каждой категории.

    :param data: Список словарей с транзакциями
    :param categories: Список категорий для подсчёта
    :return: Словарь {категория: количество}
    """
    counter = Counter()

    for transaction in data:
        description = transaction.get("description", "")

        for category in categories:
            if category.lower() in description.lower():
                counter[category] += 1

    return dict(counter)
