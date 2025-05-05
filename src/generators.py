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
