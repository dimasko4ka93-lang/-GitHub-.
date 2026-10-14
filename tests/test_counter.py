from src.counter import process_bank_operations


def test_counter_one_category():
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Открытие вклада"},
    ]
    result = process_bank_operations(data, ["Перевод"])
    assert result == {"Перевод": 2}


def test_counter_two_categories():
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    result = process_bank_operations(data, ["Перевод", "Открытие"])
    assert result == {"Перевод": 1, "Открытие": 1}


def test_counter_empty():
    result = process_bank_operations([], ["Перевод"])
    assert result == {}
