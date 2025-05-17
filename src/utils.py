import json
import os

def transactions_list(input_file):
    """Возвращает список словарей с данными о финансовых транзакциях из JSON-файла."""

    if not os.path.exists(input_file):
        return []

    try:
        with open(input_file, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return []
