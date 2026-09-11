import pytest
from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_default_executed():
    """По умолчанию возвращаются только операции со статусом EXECUTED."""
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    result = filter_by_state(data)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


def test_filter_by_state_custom_status():
    """Можно передать свой статус и получить только операции с ним."""
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    result = filter_by_state(data, "CANCELED")
    assert len(result) == 2
    assert all(op["state"] == "CANCELED" for op in result)


def test_sort_by_date_descending():
    """Сортировка по дате: по убыванию (новые сначала)."""
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    result = sort_by_date(data, reverse=True)

    # Проверяем, что даты идут по убыванию
    dates = [op["date"] for op in result]
    for i in range(len(dates) - 1):
        assert dates[i] >= dates[i + 1], f"Порядок нарушен между {i} и {i+1}"


def test_sort_by_date_ascending():
    """Сортировка по дате: по возрастанию (старые сначала)."""
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    result = sort_by_date(data, reverse=False)

    dates = [op["date"] for op in result]
    for i in range(len(dates) - 1):
        assert dates[i] <= dates[i + 1], f"Порядок нарушен между {i} и {i+1}"


def test_sort_by_date_desc():
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    result = sort_by_date(data, reverse=True)
    # Проверяем, что даты идут по убыванию
    dates = [op["date"] for op in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_asc():
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    result = sort_by_date(data, reverse=False)
    dates = [op["date"] for op in result]
    assert dates == sorted(dates, reverse=False)