import logging

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler для логов модуля
file_handler = logging.FileHandler("file_readers.log", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_csv(file_path: str) -> list:
    """
    Читает CSV-файл с транзакциями.

    :param file_path: Путь до CSV-файла
    :return: Список словарей с транзакциями
    """
    logger.info(f"Чтение CSV: {file_path}")

    try:
        df = pd.read_csv(file_path, sep=";")
        data = df.to_dict(orient="records")
        logger.info(f"Загружено записей: {len(data)}")
        return data
    except (OSError, ValueError, pd.errors.EmptyDataError) as e:
        logger.error(f"Ошибка чтения CSV: {e}")
        return []


def read_xlsx(file_path: str) -> list:
    """
    Читает XLSX-файл с транзакциями.

    :param file_path: Путь до XLSX-файла
    :return: Список словарей с транзакциями
    """
    logger.info(f"Чтение XLSX: {file_path}")

    try:
        df = pd.read_excel(file_path)
        data = df.to_dict(orient="records")
        logger.info(f"Загружено записей: {len(data)}")
        return data
    except (OSError, ValueError) as e:
        logger.error(f"Ошибка чтения XLSX: {e}")
        return []
