from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """Маскирует номер карты или счёта в строке."""

    # Проверка на пустую строку
    if not data:
        return "Вы ввели некорректный номер карты/счета"

    if data.split()[0] == "Счет":
        # Маскируем номер счёта
        number = data.split()[-1]
        if len(number) < 20 or not number.isdigit():  # Защита: номер счёта слишком короткий или не цифры
            return "Вы ввели некорректный номер счета"

        masked_number = get_mask_account(number)

        return f"Счет {masked_number}"
    else:
        # Маскируем номер карты
        parts = data.rsplit(" ", 1)
        if len(parts) != 2 or not parts[1].isdigit():  # Защита: неправильный формат строки
            return "Вы ввели некорректный номер карты"
        name = parts[0]
        number = parts[1]
        if len(number) < 16:  # Защита: номер карты слишком короткий
            return "Вы ввели некорректный номер карты"

        masked_number = get_mask_card_number(number)

        return f"{name} {masked_number}"


def get_date(date: str) -> str:
    """возвращает строку с датой в формате ДД.ММ.ГГГГ"""

    # Проверка на пустую строку
    if not date:
        return "Дата отсутствует"

    # Проверка на правильный формат с использованием strptime
    try:
        # Проверяем только часть "YYYY-MM-DD"
        datetime.strptime(date[:10], "%Y-%m-%d")
    except ValueError:
        # Если ошибка формата или недействительная дата, выбрасываем ValueError
        raise ValueError("Неверная дата")

    # Формируем строку в формате ДД.ММ.ГГГГ
    return f"{date[8:10]}.{date[5:7]}.{date[:4]}"
