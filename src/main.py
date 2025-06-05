import pandas as pd

from src.data_loader import load_transactions_from_csv, load_transactions_from_excel
from src.utils import ask_yes_no, get_transaction_amount, search_transactions_by_description, transactions_list


def main():
    """
    Основная функция программы.
    Отвечает за взаимодействие с пользователем: загрузку данных из файлов, фильтрацию по статусу,
    валюте, описанию, сортировку и вывод результата в консоль.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ").strip()

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        file_path = "data/operations.json"
        data = transactions_list(file_path)
        if not data:
            print("Не удалось загрузить данные из JSON-файла.")
            return
        df = pd.DataFrame(data)

        df["amount"] = df["operationAmount"].apply(
            lambda x: float(x["amount"]) if isinstance(x, dict) and "amount" in x else float(x)
        )
        df["currency_code"] = df["operationAmount"].apply(
            lambda x: (
                x["currency"]["code"]
                if isinstance(x, dict) and "currency" in x and isinstance(x["currency"], dict)
                else None
            )
        )

    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        file_path = "data/transactions.csv"
        try:
            df = load_transactions_from_csv(file_path)
            df.columns = df.columns.str.strip()
        except Exception as e:
            print(f"Ошибка загрузки CSV-файла: {e}")
            return

    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        file_path = "data/transactions_excel.xlsx"
        try:
            df = load_transactions_from_excel(file_path)
            df.columns = df.columns.str.strip()
        except Exception as e:
            print(f"Ошибка загрузки Excel-файла: {e}")
            return

    else:
        print("Некорректный выбор. Завершение программы.")
        return

    if df.empty:
        print("Файл пуст или не содержит данных.")
        return

    available_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = (
            input("Введите статус, по которому необходимо выполнить фильтрацию (EXECUTED, CANCELED, PENDING): ")
            .strip()
            .upper()
        )
        if status in available_statuses:
            break
        print(f'Статус "{status}" недоступен. Повторите ввод.')

    df = df[df["state"].str.upper() == status]

    if df.empty:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    df["amount_rub"] = df.apply(get_transaction_amount, axis=1)

    print(f'Операции отфильтрованы по статусу "{status}"')

    if ask_yes_no("Отсортировать операции по дате? Да/Нет: "):
        while True:
            order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
            if order in ["по возрастанию", "по убыванию"]:
                break
            print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'.")

        ascending = order == "по возрастанию"
        df = df.sort_values(by="date", ascending=ascending)

    if ask_yes_no("Выводить только рублевые транзакции? Да/Нет: "):
        df = df[df["currency_code"].str.upper() == "RUB"]

    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "):
        word = input("Введите слово для поиска в описании: ").strip()
        transactions = search_transactions_by_description(df.to_dict(orient="records"), word)
    else:
        transactions = df.to_dict(orient="records")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print("Распечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(transactions)}")
        for tx in transactions:
            date = tx.get("date", "").split("T")[0]
            description = tx.get("description", "")
            sender = tx.get("from", "")
            receiver = tx.get("to", "")
            amount = tx.get("amount", "")
            currency = tx.get("currency_code", "")
            print(f"{date} {description}")
            print(f"{sender} -> {receiver}")
            print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
