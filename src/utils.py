import json
import os
import requests
from dotenv import load_dotenv


def transactions_list(input_file):
    """Возвращает список словарей с данными о финансовых транзакциях"""
    if not os.path.exists(input_file):
        return []

    try:
        with open(input_file, encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                return []
            data = json.loads(content)
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, OSError):
        return []

    return []


load_dotenv()  # Загружаем переменные окружения из .env

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def get_transaction_amount(transaction: dict) -> float:
    """Возвращает сумму транзакции в рублях."""
    amount_str = transaction.get("operationAmount", {}).get("amount")
    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if not amount_str or not currency_code:
        return 0.0

    amount = float(amount_str)

    if currency_code == "RUB":
        return amount

    # Запрос к API для конвертации в рубли
    params = {"from": currency_code, "to": "RUB", "amount": amount}
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["result"])
    except (requests.RequestException, KeyError, ValueError):
        return 0.0
