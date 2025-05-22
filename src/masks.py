import logging
import os
from typing import Union

# Создание директории logs, если она ещё не существует
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)  # Уровень логирования не ниже DEBUG
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)  # Установка форматера

# Добавление handler к логеру
if not logger.hasHandlers():
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX"""
    card_number = str(card_number).replace(" ", "")

    if not card_number or not card_number.isdigit() or len(card_number) != 16:
        logger.error(f"Некорректный номер карты: {card_number}")
        return "Вы ввели некорректный номер карты"

    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.debug(f"Маскированный номер карты: {masked}")
    return masked


def get_mask_account(account_number: Union[str, int]) -> str:
    """Маскирует номер счёта в формате **XXXX"""
    account_number = str(account_number).replace(" ", "")

    if not account_number or not account_number.isdigit() or len(account_number) != 20:
        logger.error(f"Некорректный номер счёта: {account_number}")
        return "Вы ввели некорректный номер счета"

    masked = f"**{account_number[-4:]}"
    logger.debug(f"Маскированный номер счёта: {masked}")
    return masked
