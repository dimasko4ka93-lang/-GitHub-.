import pytest
from generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def transactions():  # <-- новое имя
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


# ... остальные фикстуры остаются без изменений


class TestFilterByCurrency:
    @pytest.mark.parametrize(
        "transactions",
        [
            "transactions_for_currency",  # 1. Имя фикстуры как строка
            [],  # 2. Пустой список напрямую
        ],
        indirect=[
            "transactions"
        ],  # 3. Говорим pytest превратить строку в вызов фикстуры
    )
    @pytest.mark.parametrize(
        "currency_code, expected_ids",
        [
            ("EUR", [2]),
            ("RUB", [1]),
            ("USD", [3]),
            ("GBP", []),
        ],
    )
    def test_filter_by_currency_various_cases(
        self, transactions, currency_code, expected_ids
    ):
        result = list(filter_by_currency(transactions, currency_code))

        actual_ids = []
        for t in result:
            if isinstance(t, dict) and "id" in t:
                actual_ids.append(t["id"])

        assert actual_ids == expected_ids


# Класс вынесен из-под TestFilterByCurrency
class TestTransactionDescriptions:
    @pytest.mark.parametrize(
        "transactions, expected_result",
        [
            # Основной сценарий со смешанными данными
            (
                [
                    {"description": "Оплата такси"},
                    {"description": ""},
                    {"description": None},
                    {"description": "Крупная покупка"},
                    {},
                ],
                ["Оплата такси", "", "", "Крупная покупка", ""],
            ),
            # НОВЫЙ СЦЕНАРИЙ: Пустой список на входе
            ([], []),
        ],
    )
    def test_extract_descriptions(self, transactions, expected_result):
        result = list(transaction_descriptions(transactions))
        assert result == expected_result


class TestCardNumberGenerator:
    @pytest.mark.parametrize(
        "start, end, expected_result",
        [
            (
                0,
                2,
                ["0000 0000 0000 0000", "0000 0000 0000 0001", "0000 0000 0000 0002"],
            ),
            (123, 123, ["0000 0000 0000 0123"]),
            (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
        ],
    )
    def test_card_number_generator_basic_ranges(self, start, end, expected_result):
        result = list(card_number_generator(start, end))
        assert result == expected_result

    @pytest.mark.parametrize(
        "start, end",
        [
            (-1, 10),
            (0, -1),
            (0, 1_000_001),
        ],
    )
    def test_card_number_generator_invalid_ranges(self, start, end):
        with pytest.raises(ValueError):
            list(card_number_generator(start, end))

    def test_card_number_generator_boundary_range_ok(self):
        result = list(card_number_generator(0, 1_000_000))
        assert len(result) == 1_000_001


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
