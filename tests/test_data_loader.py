from unittest.mock import patch

import pandas as pd

from src.data_loader import load_transactions_from_csv, load_transactions_from_excel

mock_df = pd.DataFrame([{
    "id": 1,
    "state": "EXECUTED",
    "date": "2023-01-01T00:00:00Z",
    "amount": 1000,
    "currency_name": "Ruble",
    "currency_code": "RUB",
    "from": "Счет 1",
    "to": "Счет 2",
    "description": "Перевод"
}])


@patch("os.path.exists", return_value=True)
@patch("pandas.read_csv", return_value=mock_df)
def test_load_transactions_from_csv(mock_read_csv, mock_exists):
    result = load_transactions_from_csv("test.csv")
    assert isinstance(result, list)
    assert result[0]["currency_code"] == "RUB"


@patch("os.path.exists", return_value=True)
@patch("pandas.read_excel", return_value=mock_df)
def test_load_transactions_from_excel(mock_read_excel, mock_exists):
    result = load_transactions_from_excel("test.xlsx")
    assert isinstance(result, list)
    assert result[0]["amount"] == 1000
