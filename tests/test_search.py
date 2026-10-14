from src.search import process_bank_search


def test_search_found():
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    result = process_bank_search(data, "перевод")
    assert len(result) == 1


def test_search_not_found():
    data = [{"description": "Перевод"}]
    result = process_bank_search(data, "нет такого")
    assert result == []


def test_search_empty():
    result = process_bank_search([], "тест")
    assert result == []
