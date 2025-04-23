def filter_by_state(list_of_dicts: list, state: str = "EXECUTED") -> list:
    """Функция, которая возвращает новый список словарей, содержащий только те словари, у которых ключ
    state соответствует указанному значению"""

    return [item for item in list_of_dicts if item.get("state") == state]


def sort_by_date(list_of_dicts: list, descending: bool = True) -> list:
    """Функция, которая возвращает новый список, отсортированный по дате"""

    return sorted(list_of_dicts, key=lambda item: item["date"], reverse=descending)
