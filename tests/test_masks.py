import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize("card_numbers, expected", [
    ('7000792289606361', '7000 79** **** 6361'),
    ('', 'Вы ввели некорректный номер карты'),
    ('70007bdfse06363', 'Вы ввели некорректный номер карты'),
    ('!@#$%^', 'Вы ввели некорректный номер карты'),
    ('70007922896063612', 'Вы ввели некорректный номер карты'),
])
def test_get_mask_card_number(card_numbers: int, expected: str):
    assert get_mask_card_number(card_numbers) == expected


@pytest.mark.parametrize("account_numbers, expected", [
    ('73654108430135874305', '**4305'),
    ('', 'Вы ввели некорректный номер счета'),
    ('70007bdfse06363', 'Вы ввели некорректный номер счета'),
    ('!@#$%^', 'Вы ввели некорректный номер счета'),
    ('70007922896063612', 'Вы ввели некорректный номер счета'),
])
def test_get_mask_account(account_numbers: int, expected: str):
    assert get_mask_account(account_numbers) == expected
