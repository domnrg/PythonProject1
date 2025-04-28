from typing import Union

def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Функция, которая принимает на вход номер карты и возвращает ее маску
    в формате XXXX XX** **** XXXX"""
    # Убираем пробелы и приводим к строке
    card_number = str(card_number).replace(" ", "")

    # Проверка: пустая строка, не цифры или длина не 16
    if not card_number or not card_number.isdigit() or len(card_number) != 16:
        return "Вы ввели некорректный номер карты"

    masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked_card_number

def get_mask_account(account_number: Union[str, int]) -> str:
    """Функция, которая принимает на вход номер счета и возвращает его маску
    в формате **XXXX"""
    account_number = str(account_number).replace(" ", "")

    # Проверка: пустая строка, не цифры или длина не 20
    if not account_number or not account_number.isdigit() or len(account_number) != 20:
        return "Вы ввели некорректный номер счета"

    masked_account_number = f"**{account_number[-4:]}"
    return masked_account_number