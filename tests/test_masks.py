import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.fixture
def base_card_data():
    return [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1111222233334444", "1111 22** **** 4444"),
        ("5555666677778888", "5555 66** **** 8888"),
    ]


@pytest.fixture
def base_account_data():
    return [
        ("73654108430135874305", "**4305"),
        ("98765432109876543210", "**3210"),
        ("12345678", "**5678"),
    ]


def test_get_mask_card_number_valid(base_card_data):
    for card, expected in base_card_data:
        assert get_mask_card_number(card) == expected


@pytest.mark.parametrize(
    "card",
    ["12345", "12345678901234567", "", "abcdefghij", "1234"],
)
def test_get_mask_card_number_invalid(card):
    with pytest.raises(ValueError):
        get_mask_card_number(card)


def test_get_mask_account_valid(base_account_data):
    for account, expected in base_account_data:
        assert get_mask_account(account) == expected


@pytest.mark.parametrize(
    "account",
    ["", "abc", "12", "123"],
)
def test_get_mask_account_invalid(account):
    with pytest.raises(ValueError):
        get_mask_account(account)