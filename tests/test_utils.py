import json
from unittest.mock import Mock, mock_open, patch

from src.utils import get_transaction_amount, transactions_list


@patch("os.path.exists", return_value=True)
@patch(
    "builtins.open", new_callable=mock_open, read_data=json.dumps([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}])
)
def test_transactions_list_with_valid_data(mock_file, mock_exists):
    """Проверка, что читаются корректные данные из JSON"""
    result = transactions_list("dummy_path.json")
    assert isinstance(result, list)
    assert result == [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]


@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"id": 1, "amount": 100}))
def test_transactions_list_with_not_a_list(mock_file, mock_exists):
    """Проверка, если JSON не список"""
    result = transactions_list("dummy_path.json")
    assert result == []


@patch("os.path.exists", return_value=False)
def test_transactions_list_file_not_found(mock_exists):
    """Проверка, если файл не существует"""
    result = transactions_list("nonexistent.json")
    assert result == []


@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data="")
def test_transactions_list_empty_file(mock_file, mock_exists):
    """Проверка, если JSON-файл пустой"""
    result = transactions_list("empty.json")
    assert result == []


def test_get_transaction_amount_rub():
    """Если валюта RUB — возвращается сумма без конвертации"""
    transaction = {"operationAmount": {"amount": "1000.00", "currency": {"code": "RUB"}}}
    result = get_transaction_amount(transaction)
    assert result == 1000.0


@patch("src.utils.requests.get")
def test_get_transaction_amount_foreign(mock_get):
    """Проверка конвертации валюты через API"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 9500.0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    result = get_transaction_amount(transaction)
    assert result == 9500.0
    mock_get.assert_called_once()


def test_get_transaction_amount_missing_data():
    """Неверная структура транзакции"""
    assert get_transaction_amount({}) == 0.0
    assert get_transaction_amount({"operationAmount": {}}) == 0.0
