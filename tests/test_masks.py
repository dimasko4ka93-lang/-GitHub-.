from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_valid():
    card = "7000792289606361"
    expected = "7000 79** **** 6361"
    assert get_mask_card_number(card) == expected


def test_get_mask_card_number_with_spaces():
    card = "7000 7922 8960 6361"
    expected = "7000 79** **** 6361"
    assert get_mask_card_number(card) == expected


def test_get_mask_card_number_wrong_length():
    try:
        get_mask_card_number("1234567890123")
        assert False, "Должно было выброситься исключение"
    except ValueError:
        pass


def test_get_mask_account_valid():
    account = "73654108430135874305"
    expected = "**4305"
    assert get_mask_account(account) == expected


def test_get_mask_account_with_non_digits():
    account = "AB-7365-4108-4301-3587-4305"
    expected = "**4305"
    assert get_mask_account(account) == expected
