import pytest
from src.widget import mask_account_card, get_date


@pytest.fixture
def valid_card_prefixes():
    return ["Visa Platinum", "MasterCard", "American Express"]


@pytest.mark.parametrize(
    "prefix,card_input,expected_suffix,is_valid",
    [
        ("Visa Platinum", "7000792289606361", "7000 79** **** 6361", True),
        ("MasterCard", "7000 7922 8960 6361", "7000 79** **** 6361", True),
        ("Amex", "378282246310005", "3782 82** **** 0005", False),
    ],
)
def test_mask_account_card_parametrized(prefix, card_input, expected_suffix, is_valid):
    info = f"{prefix} {card_input}"
    result = mask_account_card(info)

    digits = "".join(ch for ch in card_input if ch.isdigit())
    if is_valid and len(digits) == 16:
        assert result == f"{prefix} {expected_suffix}"
    else:
        assert result == info


def test_mask_account_card_invalid_format_no_number():
    info = "Visa Platinum"
    assert mask_account_card(info) == info


def test_mask_account_card_empty_string():
    assert mask_account_card("") == ""


def test_mask_account_card_whitespace_only():
    assert mask_account_card("   ") == ""


def test_mask_account_card_account_long():
    result = mask_account_card("Счет 73654108430135874305")
    assert result == "Счет **4305"


def test_mask_account_card_account_short():
    result = mask_account_card("Счет 123")
    assert result == "Счет 123"


def test_mask_account_card_only_digits_no_prefix():
    result = mask_account_card("7000792289606361")
    assert result == "7000 79** **** 6361"


@pytest.mark.parametrize(
    "iso_str,expected",
    [
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2020-01-15", "15.01.2020"),
        ("2023-12-31T23:59:59", "31.12.2023"),
    ],
)
def test_get_date_valid_iso(iso_str, expected):
    assert get_date(iso_str) == expected


@pytest.mark.parametrize(
    "bad_input",
    ["03.07.2019", "", "not-a-date", "2023-13-01"],
)
def test_get_date_invalid_format(bad_input):
    with pytest.raises(ValueError):
        get_date(bad_input)