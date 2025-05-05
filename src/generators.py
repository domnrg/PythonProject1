def filter_by_currency(transactions: list, currency_code: str):
    """Генератор, возвращающий транзакции с указанной валютой."""
    for transaction in transactions:
        if (
            isinstance(transaction, dict)
            and "operationAmount" in transaction
            and isinstance(transaction["operationAmount"], dict)
            and "currency" in transaction["operationAmount"]
            and isinstance(transaction["operationAmount"]["currency"], dict)
            and transaction["operationAmount"]["currency"].get("code") == currency_code
        ):
            yield transaction


def transaction_descriptions(transactions: list):
    """Генератор, который поочерёдно возвращает описание каждой транзакции."""
    for transaction in transactions:
        if "description" in transaction:
            yield transaction["description"]


def card_number_generator(start: int, end: int):
    """Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX."""
    for number in range(start, end + 1):
        # Преобразуем число в строку длиной 16 символов, дополняя нулями слева
        formatted = f"{number:016d}"
        # Разбиваем строку на группы по 4 цифры
        yield f"{formatted[:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:]}"