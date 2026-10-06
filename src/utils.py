import json
import logging
import os

from src.file_readers import read_csv, read_xlsx

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler для логов модуля
file_handler = logging.FileHandler("utils.log", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_operations(file_path: str) -> list:
    """
    Загружает список финансовых транзакций из файла.

    Поддерживает форматы: JSON, CSV, XLSX.

    :param file_path: Путь до файла
    :return: Список словарей с транзакциями или пустой список
    """
    logger.info(f"Загрузка операций из файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    # Определяем расширение
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".json":
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Ошибка чтения JSON: {e}")
            return []
    elif extension == ".csv":
        data = read_csv(file_path)
    elif extension == ".xlsx":
        data = read_xlsx(file_path)
    else:
        logger.error(f"Неподдерживаемый формат: {extension}")
        return []

    if not isinstance(data, list):
        logger.warning(f"Данные не являются списком: {type(data)}")
        return []

    logger.info(f"Загружено операций: {len(data)}")
    return data
