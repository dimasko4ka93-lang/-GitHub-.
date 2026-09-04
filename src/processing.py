from datetime import datetime
from typing import Any, Dict, List, Optional


def filter_by_state(
    operations: List[Dict[str, Any]],
    state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Возвращает список операций, у которых ключ 'state' равен указанному значению.

    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(
    operations: List[Dict[str, Any]],
    reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате (ключ 'date') и возвращает новый отсортированный список.

    """
    def _parse_date(op: Dict[str, Any]) -> datetime:
        date_str = op.get("date", "")
        # fromisoformat корректно обрабатывает микросекунды
        return datetime.fromisoformat(date_str)

    return sorted(operations, key=_parse_date, reverse=reverse)