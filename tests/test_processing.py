import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def operations_data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state_default_executed(operations_data):
    """По умолчанию возвращаются только операции со статусом EXECUTED."""
    result = filter_by_state(operations_data)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


def test_filter_by_state_custom_status(operations_data):
    """Можно передать свой статус и получить только операции с ним."""
    result = filter_by_state(operations_data, "CANCELED")
    assert len(result) == 2
    assert all(op["state"] == "CANCELED" for op in result)


def test_sort_by_date_descending(operations_data):
    """Сортировка по дате: по убыванию (новые сначала)."""
    result = sort_by_date(operations_data, reverse=True)

    dates = [op["date"] for op in result]
    for i in range(len(dates) - 1):
        assert dates[i] >= dates[i + 1], f"Порядок нарушен между {i} и {i+1}"


def test_sort_by_date_ascending(operations_data):
    """Сортировка по дате: по возрастанию (старые сначала)."""
    result = sort_by_date(operations_data, reverse=False)

    dates = [op["date"] for op in result]
    for i in range(len(dates) - 1):
        assert dates[i] <= dates[i + 1], f"Порядок нарушен между {i} и {i+1}"