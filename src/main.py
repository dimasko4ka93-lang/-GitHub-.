import json

from src.search import process_bank_search


def load_data():
    """Загружает данные из файла."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ")

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        with open("data/operations.json", "r", encoding="utf-8") as f:
            return json.load(f)
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        from src.file_readers import read_csv
        return read_csv("data/transactions.csv")
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        from src.file_readers import read_xlsx
        return read_xlsx("data/transactions_excel.xlsx")
    else:
        print("Неверный выбор")
        return []


def main():
    """Основная логика программы."""
    data = load_data()
    if not data:
        print("Нет данных")
        return

    # Фильтрация по статусу
    status = input("Введите статус: ").upper()
    while status not in ("EXECUTED", "CANCELED", "PENDING"):
        print(f'Статус "{status}" недоступен.')
        status = input("Введите статус: ").upper()

    data = [t for t in data if t.get("state") == status]
    print(f'Операции отфильтрованы по статусу "{status}"')

    # Сортировка
    if input("Отсортировать по дате? Да/Нет: ").lower() == "да":
        order = input("По возрастанию или убыванию? ").lower()
        reverse = order == "убыванию"
        data.sort(key=lambda x: x.get("date", ""), reverse=reverse)

    # Фильтр по валюте
    if input("Выводить только рублёвые? Да/Нет: ").lower() == "да":
        data = [
            t for t in data
            if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    # Поиск по описанию
    if input("Фильтровать по слову в описании? Да/Нет: ").lower() == "да":
        search = input("Введите слово: ")
        data = process_bank_search(data, search)

    # Вывод
    print(f"\nВсего операций: {len(data)}")

    if not data:
        print("Не найдено ни одной транзакции")
    else:
        for t in data:
            date = t.get("date", "")[:10]
            description = t.get("description", "")
            amount = t.get("operationAmount", {}).get("amount", "")
            currency = t.get("operationAmount", {}).get("currency", {}).get("name", "")

            print(f"\n{date} {description}")
            print(f"Сумма: {amount} {currency}")


if __name__ == "__main__":
    main()
