import json
import os


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
