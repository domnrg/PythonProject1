import pandas as pd
import os


def load_transactions_from_csv(file_path: str) -> pd.DataFrame:
    """Загружает транзакции из CSV-файла."""
    if not os.path.exists(file_path) or not file_path.endswith(".csv"):
        raise ValueError("Неверный путь к CSV-файлу или неподдерживаемый формат.")
    return pd.read_csv(file_path)


def load_transactions_from_excel(file_path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла."""
    if not os.path.exists(file_path) or not file_path.endswith((".xls", ".xlsx")):
        raise ValueError("Неверный путь к Excel-файлу или неподдерживаемый формат.")
    return pd.read_excel(file_path)
