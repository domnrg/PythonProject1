from types import GeneratorType

from src.generators import filter_by_currency, transaction_descriptions

def test_filter_by_currency_usd(sample_transactions):
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert len(result) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)


def test_filter_by_currency_eur(sample_transactions):
    result = list(filter_by_currency(sample_transactions, "EUR"))
    assert len(result) == 1
    assert result[0]["operationAmount"]["currency"]["code"] == "EUR"


def test_filter_by_currency_rub(sample_transactions):
    result = list(filter_by_currency(sample_transactions, "RUB"))
    assert len(result) == 1
    assert result[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_not_found(sample_transactions):
    result = list(filter_by_currency(sample_transactions, "JPY"))
    assert result == []

def test_filter_by_currency_invalid_structures(sample_transactions):
    # Проверка, что функция не ломается на некорректных словарях
    result = list(filter_by_currency(sample_transactions, "USD"))
    ids = [t["id"] for t in result]
    assert 5 not in ids
    assert 6 not in ids
    assert 7 not in ids

def test_filter_by_currency_stop_iteration(sample_transactions):
    gen = filter_by_currency(sample_transactions, "USD")
    next(gen)  # первый
    next(gen)  # второй
    with pytest.raises(StopIteration):
        next(gen)  # должен завершиться


def test_transaction_descriptions_output(transactions_with_descriptions):
    result = list(transaction_descriptions(transactions_with_descriptions))
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Оплата услуг"
    ]

def test_transaction_descriptions_iterator(transactions_with_descriptions):
    gen = transaction_descriptions(transactions_with_descriptions)
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert isinstance(gen, GeneratorType)  # Проверка, что это генератор
