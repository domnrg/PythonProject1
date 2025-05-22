import os
import logging
from typing import Union

# Создаём директорию logs, если её нет
os.makedirs("logs", exist_ok=True)

# Настройка логирования
log_file_path = os.path.join("logs", "masks.log")

logging.basicConfig(
    filename=log_file_path,
    filemode="w",  # Перезапись при запуске
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Возвращает маску номера карты в формате XXXX XX** **** XXXX"""
    card_number = str(card_number).replace(" ", "")

    if not card_number or not card_number.isdigit() or len(card_number) != 16:
        logger.warning("Некорректный номер карты: %s", card_number)
        return "Вы ввели некорректный номер карты"

    masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info("Карта успешно замаскирована.")
    return masked_card_number


def get_mask_account(account_number: Union[str, int]) -> str:
    """Возвращает маску номера счёта в формате **XXXX"""
    account_number = str(account_number).replace(" ", "")

    if not account_number or not account_number.isdigit() or len(account_number) != 20:
        logger.warning("Некорректный номер счёта: %s", account_number)
        return "Вы ввели некорректный номер счета"

    masked_account_number = f"**{account_number[-4:]}"
    logger.info("Счёт успешно замаскирован.")
    return masked_account_number
