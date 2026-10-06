import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем обработчик файла
file_handler = logging.FileHandler("utils.log", encoding="utf-8")

file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# привязываем форматер к обработчику
file_handler.setFormatter(file_formatter)
# Добоваляем обработчик к логгеру
logger.addHandler(file_handler)


def load_operations(file_path: str) -> list:
    """
    Загружает список финансовых транзакций из JSON-файла.

    :param file_path: Путь до JSON-файла
    :return: Список словарей с транзакциями или пустой список
    """
    # 1. Проверяем, существует ли файл
    logger.info(f"Загрузка операций из файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Ошибка чтения файла: {e}")
        return []

    if not isinstance(data, list):
        logger.warning(f"Данные не являются списком: {type(data)}")
        return []

    logger.info(f"Загружено операций: {len(data)}")
    return data
