import pytest
from generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


class TestFilterByCurrency:
    @staticmethod
    def sample_transactions():
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
                "operationAmount": "invalid_structure",  # Не dict
            },
            {
                "id": 5,
                "description": "Транзакция без кода валюты",
                "operationAmount": {"currency": {}},
            },
        ]

    # 1. test_filter_by_currency_eur
    def test_filter_by_currency_eur(self):
        transactions = self.sample_transactions()
        result = list(filter_by_currency(transactions, "EUR"))
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_by_currency_rub(self):
        transactions = self.sample_transactions()
        result = list(filter_by_currency(transactions, "RUB"))
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_filter_by_currency_skips_invalid_structures(self):
        transactions = self.sample_transactions()
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 1
        assert result[0]["id"] == 3

    def test_filter_by_currency_skips_invalid_structures(self):
        transactions = self.sample_transactions()
        # В списке есть транзакция с id=4 (operationAmount не dict) и id=5 (нет code)
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 1
        assert result[0]["id"] == 3

    def test_filter_by_currency_empty_list(self):
        result = list(filter_by_currency([], "USD"))  # <-- было transactions (не определено)
        assert result == []


class TestTransactionDescriptions:
    @staticmethod
    def sample_transactions():
        return [
            {"description": "Оплата такси"},
            {"description": ""},
            {"description": None},
            {"description": "Крупная покупка"},
            {},  # Нет ключа description
        ]

    def test_transaction_descriptions_normal_cases(self):
        transactions = self.sample_transactions()
        result = list(transaction_descriptions(transactions))
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
            list(card_number_generator(0, 1_000_001))  # Разница > 1_000_000

    def test_card_number_generator_boundary_range_ok(self):
        # Диапазон ровно 1_000_000 элементов (от 0 до 1_000_000 включительно)
        result = list(card_number_generator(0, 1_000_000))
        assert len(result) == 1_000_001


if __name__ == "__main__":
    pytest.main([__file__, "-v"])