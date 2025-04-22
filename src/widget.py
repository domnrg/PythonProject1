from masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """Маскирует номер карты или счёта в строке."""

    if data.split()[0] == "Счет":
        # Маскируем номер счёта
        number = data.split()[-1]
        masked_number = get_mask_account(number)

        return f"Счет {masked_number}"
    else:
        # Маскируем номер карты
        parts = data.rsplit(" ", 1)
        name = parts[0]
        number = parts[1]
        masked_number = get_mask_card_number(number)

        return f"{name} {masked_number}"


def get_date(date: str) -> str:
    """возвращает строку с датой в формате ДД.ММ.ГГГГ"""

    return f"{date[8:10]}.{date[5:7]}.{date[:4]}"
