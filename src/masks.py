import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаём обработчик файла
file_handler = logging.FileHandler("masks.log", encoding="utf-8")

# Форматер
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card: str) -> str:
    """
    Маскирует номер карты в формате: XXXX XX** **** XXXX
    Видны первые 6 и последние 4 цифры.
    Пример: 7000792289606361 → 7000 79** **** 6361
    """
    logger.info(f"Маскировка карты: {card}")

    digits = "".join(ch for ch in card if ch.isdigit())

    if len(digits) != 16:
        logger.error(f"Неверная длина номера карты: {len(digits)} цифр")
        raise ValueError("Номер карты должен содержать ровно 16 цифр.")

    first_6 = digits[:6]
    last_4 = digits[-4:]

    part1 = first_6[:4]
    part2 = first_6[4:] + "**"
    part3 = "****"
    part4 = last_4

    masked = f"{part1} {part2} {part3} {part4}"
    logger.info(f"Результат маскировки: {masked}")
    return masked


def get_mask_account(account: str) -> str:
    """
    Маскирует номер счёта в формате: **XXXX
    Видны только последние 4 цифры, перед ними две звёздочки.
    Пример: 73654108430135874305 → **4305
    """
    logger.info(f"Маскировка счёта: {account}")

    digits = "".join(ch for ch in account if ch.isdigit())

    if len(digits) < 4:
        logger.error(f"Слишком короткий номер счёта: {len(digits)} цифр")
        raise ValueError("Номер счёта должен содержать не менее 4 цифр.")

    last_4 = digits[-4:]
    masked = f"**{last_4}"
    logger.info(f"Результат маскировки: {masked}")
    return masked
