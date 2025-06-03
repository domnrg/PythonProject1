import json
import logging
import os
import re
from typing import List, Dict

import requests
from dotenv import load_dotenv

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


def get_transaction_amount(transaction: dict) -> float:
    """Возвращает сумму транзакции в рублях."""
    amount_str = transaction.get("operationAmount", {}).get("amount")
    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if not amount_str or not currency_code:
        logger.warning("Отсутствуют данные о сумме или валюте")
        return 0.0

    amount = float(amount_str)

    if currency_code == "RUB":
        return amount

    params = {"from": currency_code, "to": "RUB", "amount": amount}
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        result = float(data["result"])
        logger.debug(f"Конвертировано {amount} {currency_code} в {result} RUB")
        return result
    except (requests.RequestException, KeyError, ValueError) as e:
        logger.error(f"Ошибка конвертации валюты: {e}")
        return 0.0


def search_transactions_by_description(transactions: List[Dict], keyword: str) -> List[Dict]:
    """Возвращает транзакции, в описании которых содержится заданное слово."""
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return [tx for tx in transactions if pattern.search(tx.get("description", ""))]


def count_transactions_by_category(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Считает количество транзакций по категориям."""
    category_count = {category: 0 for category in categories}
    for tx in transactions:
        description = tx.get("description", "").strip().lower()
        for category in categories:
            if category.lower() in description:
                category_count[category] += 1
    return category_count

