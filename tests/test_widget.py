import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "data, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("", "Вы ввели некорректный номер карты/счета"),
        ("Visa Platinum 70007922", "Вы ввели некорректный номер карты"),
        ("Maestro 1596837868705abc", "Вы ввели некорректный номер карты"),
        ("Счет 736541084301358", "Вы ввели некорректный номер счета"),
        ("Счет 7365410843013587430b", "Вы ввели некорректный номер счета"),
    ],
)
def test_mask_account_card(data: str, expected: str):
    assert mask_account_card(data) == expected


@pytest.mark.parametrize("date, expected", [("2024-03-11T02:26:18.671407", "11.03.2024"), ("", "Дата отсутствует")])
def test_get_date_valid(date: str, expected: str):
    assert get_date(date) == expected

def test_get_date_invalid_format():
    with pytest.raises(ValueError):
        get_date("2024.03.11")  # Неверный формат

def test_get_date_invalid_date():
    with pytest.raises(ValueError):
        get_date("2024-02-30T02:26:18.671407")  # Некорректная дата
