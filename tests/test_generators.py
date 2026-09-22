import pytest
from generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def transactions_for_currency():
    return [
        {
            "id": 1,
            "description": "Покупка кофе",
            "operationAmount": {"currency": {"code": "RUB"}, "value": 300},
        },
        {
            "id": 2,
            "description": "Оплата отеля",
            "operationAmount": {"currency": {"code": "EUR"}, "value": 100},
        },
        {
            "id": 3,
            "description": "Перевод другу",
            "operationAmount": {"currency": {"code": "USD"}, "value": 50},
        },
        {
            "id": 4,
            "description": "Транзакция с битыми данными",
            "operationAmount": "invalid_structure",
        },
        {
            "id": 5,
            "description": "Транзакция без кода валюты",
            "operationAmount": {"currency": {}},
        },
    ]


@pytest.fixture
def transactions_for_descriptions():
    return [
        {"description": "Оплата такси"},
        {"description": ""},
        {"description": None},
        {"description": "Крупная покупка"},
        {},
    ]


class TestFilterByCurrency:
    def test_filter_by_currency_eur(self, transactions_for_currency):
        result = list(filter_by_currency(transactions_for_currency, "EUR"))
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_by_currency_rub(self, transactions_for_currency):
        result = list(filter_by_currency(transactions_for_currency, "RUB"))
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_filter_by_currency_skips_invalid_structures(self, transactions_for_currency):
        result = list(filter_by_currency(transactions_for_currency, "USD"))
        assert len(result) == 1
        assert result[0]["id"] == 3

    def test_filter_by_currency_empty_list(self):
        result = list(filter_by_currency([], "USD"))
        assert result == []


class TestTransactionDescriptions:
    def test_transaction_descriptions_normal_cases(self, transactions_for_descriptions):
        result = list(transaction_descriptions(transactions_for_descriptions))
        assert result == ["Оплата такси", "", "", "Крупная покупка", ""]

    def test_transaction_descriptions_empty_list(self):
        result = list(transaction_descriptions())
        assert len(result) == 0


class TestCardNumberGenerator:
    def test_card_number_generator_basic_range(self):
        result = list(card_number_generator(0, 2))
        assert result == [
            "0000 0000 0000 0000",
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
        ]

    def test_card_number_generator_single_value(self):
        result = list(card_number_generator(123, 123))
        assert result == ["0000 0000 0000 0123"]

    def test_card_number_generator_large_number_formatting(self):
        result = list(card_number_generator(9999999999999999, 9999999999999999))
        assert result == ["9999 9999 9999 9999"]

    def test_card_number_generator_negative_start_raises(self):
        with pytest.raises(ValueError):
            list(card_number_generator(-1, 10))

    def test_card_number_generator_negative_end_raises(self):
        with pytest.raises(ValueError):
            list(card_number_generator(0, -1))

    def test_card_number_generator_range_too_large_raises(self):
        with pytest.raises(ValueError):
            list(card_number_generator(0, 1_000_001))

    def test_card_number_generator_boundary_range_ok(self):
        result = list(card_number_generator(0, 1_000_000))
        assert len(result) == 1_000_001


if __name__ == "__main__":
    pytest.main([__file__, "-v"])