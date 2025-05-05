import pytest


@pytest.fixture
def operations_data():
    """Тестовые данные для функции filter_by_state"""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 123456789, "date": "2020-01-01T00:00:00.000000"},  # Без ключа 'state'
        {"id": 987654321, "state": None, "date": "2021-01-01T00:00:00.000000"},  # Некорректное значение state
        {"id": 999999999, "state": "EXECUTED", "date": "2018-10-14T08:21:33.419441"},  # одинаковая дата
        {"id": 888888888, "state": "EXECUTED", "date": "неправильная_дата"}  # некорректная дата
    ]


@pytest.fixture
def sample_transactions():
    """Тестовые данные для функции filter_by_currency"""
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "1000.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "2000.00",
                "currency": {
                    "name": "EUR",
                    "code": "EUR"
                }
            }
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "3000.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        },
        {
            "id": 4,
            "operationAmount": {
                "amount": "4000.00",
                "currency": {
                    "name": "RUB",
                    "code": "RUB"
                }
            }
        },
        {
            "id": 5,
            # отсутствует ключ "operationAmount"
        },
        {
            "id": 6,
            "operationAmount": {
                # отсутствует "currency"
            }
        },
        {
            "id": 7,
            "operationAmount": {
                "currency": {
                    # отсутствует "code"
                }
            }
        }
    ]


@pytest.fixture
def transactions_with_descriptions():
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Перевод с карты на карту"},
        {"id": 4},  # нет description
        {"id": 5, "description": "Оплата услуг"}
    ]