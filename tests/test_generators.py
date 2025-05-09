from types import GeneratorType

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


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
    assert result == ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту", "Оплата услуг"]


def test_transaction_descriptions_iterator(transactions_with_descriptions):
    gen = transaction_descriptions(transactions_with_descriptions)
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert isinstance(gen, GeneratorType)  # Проверка, что это генератор


def test_card_number_generator_type():
    gen = card_number_generator(1, 1)
    assert isinstance(gen, GeneratorType)  # Проверка, что это генератор


@pytest.mark.parametrize("start, end", [(1, 3), (9999999999999997, 9999999999999999)])
def test_card_number_format_and_range(start, end):
    result = list(card_number_generator(start, end))
    expected_count = end - start + 1
    assert len(result) == expected_count

    for card in result:
        assert len(card) == 19  # Длина должна быть 19 символов включая пробелы
        assert card.count(" ") == 3  # Формат должен содержать три пробела
        assert all(part.isdigit() and len(part) == 4 for part in card.split())  # Каждая часть должна быть из 4 цифр

        number = int(card.replace(" ", ""))
        assert start <= number <= end  # Число вне диапазона"


def test_card_number_generator_empty_range():
    result = list(card_number_generator(10, 5))
    assert result == []  # Если начальное значение больше конечного, результат должен быть пустым


def test_card_number_generator_example_range():
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    result = list(card_number_generator(1, 5))
    assert result == expected
