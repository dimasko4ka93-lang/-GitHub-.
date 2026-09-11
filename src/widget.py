from datetime import datetime

from src.masks import get_mask_account as _mask_account_number
from src.masks import get_mask_card_number as _mask_card_number


def mask_account_card(info: str) -> str:
    """
    Принимает строку вида:
      - "Visa Platinum 7000792289606361"
      - "Visa Platinum 7000 7922 8960 6361"
      - "Счет 73654108430135874305"

    Определяет тип (карта или счёт) и применяет маскировку.
    Пробелы в номере игнорируются.
    """
    info_stripped = info.strip()
    if not info_stripped:
        return info_stripped

    # Собираем ВСЕ цифры из строки
    digits = "".join(ch for ch in info_stripped if ch.isdigit())

    if info_stripped.startswith("Счет"):
        if len(digits) >= 4:
            masked_number = _mask_account_number(digits)
            return f"Счет {masked_number}"
        return info_stripped
    else:
        if len(digits) == 16:
            masked_number = _mask_card_number(digits)
            # Сохраняем текст до номера (префикс карты)
            prefix = "".join(ch for ch in info_stripped if not ch.isdigit()).strip()
            if prefix:
                return f"{prefix} {masked_number}"
            return masked_number
        return info_stripped


def get_date(iso_datetime_str: str) -> str:
    dt = datetime.fromisoformat(iso_datetime_str)
    return dt.strftime("%d.%m.%Y")
