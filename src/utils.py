import json
import logging
import os
import re
from typing import List, Dict

import pandas as pd
import requests
from dotenv import load_dotenv
from collections import Counter

# Создание папки logs, если нет
os.makedirs("logs", exist_ok=True)

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)

# Избегаем дублирования хендлеров
if not logger.handlers:
    logger.addHandler(file_handler)

load_dotenv()  # Загружаем переменные окружения из .env

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def transactions_list(input_file):
    """Возвращает список словарей с данными о финансовых транзакциях"""
    if not os.path.exists(input_file):
        logger.warning(f"Файл не найден: {input_file}")
        return []

    try:
        with open(input_file, encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                logger.info(f"Файл пустой: {input_file}")
                return []
            data = json.loads(content)
            if isinstance(data, list):
                logger.debug(f"Успешно загружено {len(data)} транзакций из {input_file}")
                return data
            else:
                logger.warning("Ожидался список транзакций, получено что-то другое")
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Ошибка чтения файла {input_file}: {e}")

    return []


def get_transaction_amount(row: pd.Series) -> float:
    """Возвращает сумму транзакции в рублях для строки DataFrame."""
    try:
        amount_str = row["operationAmount"]["amount"]
        currency_code = row["operationAmount"]["currency"]["code"]
    except (KeyError, TypeError):
        logger.warning("Ошибка при извлечении суммы или валюты")
        return 0.0

    try:
        amount = float(amount_str)
    except ValueError:
        logger.error(f"Невозможно преобразовать сумму: {amount_str}")
        return 0.0

    if currency_code == "RUB":
        return amount

    # Конвертация через API
    params = {"from": currency_code, "to": "RUB", "amount": amount}
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["result"])
    except (requests.RequestException, KeyError, ValueError) as e:
        logger.error(f"Ошибка конвертации валюты: {e}")
        return 0.0


def search_transactions_by_description(transactions: List[Dict], keyword: str) -> List[Dict]:
    """Возвращает транзакции, в описании которых содержится заданное слово."""
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return [tx for tx in transactions if pattern.search(tx.get("description", ""))]


def count_transactions_by_category(transactions: list[dict], categories: list[str]) -> dict:
    """Возвращает количество операций в каждой категории из переданного списка."""
    counter = Counter()
    for tx in transactions:
        description = tx.get("description", "")
        if description in categories:
            counter[description] += 1
    return dict(counter)


def ask_yes_no(prompt: str) -> bool:
    """Спрашивает у пользователя 'да' или 'нет' и возвращает True/False"""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        elif answer in ("нет", "н", "no", "n"):
            return False
        print("Пожалуйста, введите 'да' или 'нет'.")
