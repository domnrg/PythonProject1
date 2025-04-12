from typing import Union


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Функция, которая принимает на вход номер карты и возвращает ее маску
    в формате XXXX XX** **** XXXX"""
    # Убираем пробелы и приводим к строке (если вдруг передали int)
    card_number = str(card_number).replace(" ", "")

    masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked_card_number


def get_mask_account(account_number: Union[str, int]) -> str:
    """Функция, которая принимает на вход номер счета и возвращает его маску
    в формате **XXXX"""
    # Убираем пробелы и приводим к строке (если вдруг передали int)
    account_number = str(account_number).replace(" ", "")

    masked_account_number = f"**{account_number[-4:]}"
    return masked_account_number
