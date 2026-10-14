from unittest.mock import patch

from src.main import main


@patch("src.main.load_data")
@patch("builtins.input")
def test_main_no_data(mock_input, mock_load):
    """Если данных нет — сообщение."""
    mock_load.return_value = []
    mock_input.return_value = "1"

    main()  # не должно упасть


@patch("src.main.load_data")
@patch("builtins.input")
def test_main_simple(mock_input, mock_load):
    """Простой сценарий."""
    mock_load.return_value = [
        {"state": "EXECUTED", "date": "2024-01-01T00:00:00",
         "description": "Перевод", "operationAmount": {
             "amount": "100", "currency": {"code": "RUB", "name": "руб."}}},
    ]
    # Ответы: статус, сортировка, валюта, поиск
    mock_input.side_effect = ["1", "EXECUTED", "нет", "нет", "нет"]

    main()
