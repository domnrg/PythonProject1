import json
from unittest.mock import Mock, mock_open, patch

import pytest

from src.utils import (count_transactions_by_category, get_transaction_amount, search_transactions_by_description,
                       transactions_list)


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


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата товаров"},
        {"id": 3, "description": "перевод со счета на счет"},
        {"id": 4, "description": "Снятие наличных"},
        {"id": 5, "description": ""},
    ]


def test_search_description_found(sample_transactions):
    result = search_transactions_by_description(sample_transactions, "перевод")
    assert len(result) == 2
    assert all("перевод" in tx["description"].lower() for tx in result)


def test_search_description_case_insensitive(sample_transactions):
    result = search_transactions_by_description(sample_transactions, "ОрГаНиЗаЦиИ")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_search_description_not_found(sample_transactions):
    result = search_transactions_by_description(sample_transactions, "нечто")
    assert result == []


def test_search_description_empty(sample_transactions):
    result = search_transactions_by_description(sample_transactions, "")
    # Все, у кого description не пустой, попадут
    assert len(result) == 5


def test_count_transactions_by_category_basic(sample_transactions):
    result = count_transactions_by_category(sample_transactions)
    assert isinstance(result, dict)
    assert result["перевод организации"] == 1
    assert result["перевод со счета на счет"] == 1
    assert result["оплата товаров"] == 1
    assert result["снятие наличных"] == 1
    assert "" in result  # пустая строка — тоже учитывается


def test_count_transactions_empty():
    assert count_transactions_by_category([]) == {}
