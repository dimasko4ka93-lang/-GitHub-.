from datetime import datetime

from src.masks import get_mask_account as _mask_account_number
from src.masks import get_mask_card_number as _mask_card_number


def mask_account_card(info: str) -> str:
    """
    Принимает одну строку вида:
      - "Visa Platinum 7000792289606361"
      - "Счет 73654108430135874305"

    Определяет тип (карта или счёт) и применяет соответствующую маскировку
    через переиспользуемые функции из src/masks.py.
    """
    info_stripped = info.strip()

    if info_stripped.startswith("Счет"):
        parts = info_stripped.split()
        if len(parts) < 2:
            return info_stripped

        account_number = parts[-1]
        # Вызываем твою функцию get_mask_account через алиас _mask_account_number
        masked_number = _mask_account_number(account_number)
        return f"Счет {masked_number}"

    else:
        parts = info_stripped.split()
        if len(parts) < 2:
            return info_stripped

        card_number = parts[-1]
        # Вызываем твою функцию get_mask_card_number через алиас _mask_card_number
        masked_number = _mask_card_number(card_number)

        base_text = " ".join(parts[:-1])
        return f"{base_text} {masked_number}"

def get_date(iso_datetime_str: str) -> str:
    dt = datetime.fromisoformat(iso_datetime_str)
    return dt.strftime("%d.%m.%Y")
