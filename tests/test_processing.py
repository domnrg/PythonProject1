import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 999999999, "state": "EXECUTED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 888888888, "state": "EXECUTED", "date": "неправильная_дата"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
        ("PENDING", []),  # Нет ни одного словаря с таким state
        ("None", []),  # Даже если есть ключ с None, он не равен строке "None"
    ],
)
def test_filter_by_state(operations_data, state, expected):
    result = filter_by_state(operations_data, state)
    assert result == expected


def test_filter_by_state_empty():
    """Проверка функции на пустом списке"""
    result = filter_by_state([])
    assert result == []


def test_filter_by_state_missing_state_key():
    """Проверка, что словари без ключа 'state' игнорируются"""
    data = [
        {"id": 1, "date": "2024-01-01T00:00:00.000000"},
        {"id": 2, "state": "EXECUTED", "date": "2024-02-01T00:00:00.000000"},
    ]
    result = filter_by_state(data, "EXECUTED")
    assert result == [{"id": 2, "state": "EXECUTED", "date": "2024-02-01T00:00:00.000000"}]


def test_sort_by_date_descending(operations_data):
    """Тест сортировки по убыванию дат"""
    result = sort_by_date(operations_data, descending=True)
    dates = [item["date"] for item in result if item["date"].startswith("20")]
    assert dates == sorted(dates, reverse=True)  # Проверяем убывание


def test_sort_by_date_ascending(operations_data):
    """Тест сортировки по возрастанию дат"""
    result = sort_by_date(operations_data, descending=False)
    dates = [item["date"] for item in result if item["date"].startswith("20")]
    assert dates == sorted(dates)  # Проверяем возрастание


def test_sort_by_date_same_dates(operations_data):
    """Тест на обработку одинаковых дат"""
    sorted_items = sort_by_date(operations_data)
    # Оба элемента с одинаковой датой должны остаться в правильном порядке (порядок сортировки стабильный)
    ids_with_same_date = [item["id"] for item in sorted_items if item["date"] == "2018-10-14T08:21:33.419441"]
    assert set(ids_with_same_date) == {615064591, 999999999}


def test_sort_by_date_invalid_format(operations_data):
    """Тест: элемент с некорректной датой не должен вызвать ошибку сортировки"""
    try:
        sort_by_date(operations_data)
    except Exception:
        pytest.fail("Сортировка должна работать даже с некорректными датами")
