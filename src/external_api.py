import os

import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env


def convert_to_rub(amount: float, from_currency: str) -> float:
    url = "https://api.apilayer.com/exchangerates_data/convert"
    params = {"from": from_currency, "to": "RUB", "amount": amount}
    headers = {"apikey": os.getenv("EXCHANGE_API_KEY")}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data.get("success"):
        return data["result"]
    return 0.0
