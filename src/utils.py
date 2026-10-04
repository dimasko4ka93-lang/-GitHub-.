import json
import os


def load_operations(file_path: str) -> list:
    """
    Загружает список финансовых транзакций из JSON-файла.

    :param file_path: Путь до JSON-файла
    :return: Список словарей с транзакциями или пустой список
    """
    # 1. Проверяем, существует ли файл
    if not os.path.exists(file_path):
        return []

    # 2. Пытаемся открыть и прочитать файл
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        # Если файл пустой, битый JSON или нет доступа
        return []

    # 3. Проверяем, что данные — это список
    if not isinstance(data, list):
        return []

    # 4. Возвращаем список транзакций
    return data
