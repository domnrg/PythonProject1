import json
from unittest.mock import mock_open, patch
from src.utils import transactions_list


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
