from unittest.mock import MagicMock, patch

from src.external_api import get_transaction_amount_in_rub


def test_rub_transaction():
    """RUB — без запроса к API."""
    transaction = {
        "operationAmount": {
            "amount": "1000",
            "currency": {"code": "RUB"}
        }
    }
    result = get_transaction_amount_in_rub(transaction)
    assert result == 1000.0


@patch('src.external_api.requests.get')
def test_usd_transaction(mock_get):
    """USD — запрос к API (замокан)."""
    # Настраиваем mock
    mock_response = MagicMock()
    mock_response.text = '''<?xml version="1.0" encoding="windows-1251"?>
    <ValCurs>
        <Valute>
            <CharCode>USD</CharCode>
            <Nominal>1</Nominal>
            <Value>90,00</Value>
        </Valute>
    </ValCurs>'''
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }
    result = get_transaction_amount_in_rub(transaction)

    assert result == 9000.0
    mock_get.assert_called_once()


@patch('src.external_api.requests.get')
def test_eur_transaction(mock_get):
    """EUR — запрос к API (замокан)."""
    mock_response = MagicMock()
    mock_response.text = '''<?xml version="1.0" encoding="windows-1251"?>
    <ValCurs>
        <Valute>
            <CharCode>EUR</CharCode>
            <Nominal>1</Nominal>
            <Value>100,00</Value>
        </Valute>
    </ValCurs>'''
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "50",
            "currency": {"code": "EUR"}
        }
    }
    result = get_transaction_amount_in_rub(transaction)

    assert result == 5000.0
    mock_get.assert_called_once()
