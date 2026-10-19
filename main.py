import json

from src.file_readers import read_csv, read_xlsx
from src.masks import get_mask_account, get_mask_card_number
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
        try:
            with open("data/operations.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")

        return read_csv("data/transactions.csv")
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")

        return read_xlsx("data/transactions_excel.xlsx")
    else:
        print("Неверный выбор")
        return []


def format_transaction(transaction):
    """Красиво форматирует одну транзакцию (с маскировкой)."""
    date = transaction.get("date", "")[:10]
    description = transaction.get("description", "")

    # Получаем данные из JSON или CSV
    if "operationAmount" in transaction:
        amount = transaction["operationAmount"].get("amount", "")
        currency = transaction["operationAmount"].get("currency", {}).get("name", "")
    else:
        amount = transaction.get("amount", "")
        currency = transaction.get("currency_name", "")

    # Маскируем откуда и куда
    from_acc = transaction.get("from", "")
    to_acc = transaction.get("to", "")

    # Применяем маскировку в зависимости от того, карта это или счет
    if from_acc:
        if from_acc.startswith("Счет"):
            # Оставляем слово "Счет" и маскируем цифры
            digits = "".join(ch for ch in from_acc if ch.isdigit())
            if len(digits) >= 4:
                from_acc = f"Счет {get_mask_account(digits)}"
        else:
            # Это карта, отрезаем название платежной системы и маскируем
            digits = "".join(ch for ch in from_acc if ch.isdigit())
            if len(digits) == 16:
                name = "".join(ch for ch in from_acc
                               if ch.isalpha() or ch.isspace()).strip()
                from_acc = f"{name} {get_mask_card_number(digits)}"

    if to_acc:
        if to_acc.startswith("Счет"):
            digits = "".join(ch for ch in to_acc if ch.isdigit())
            if len(digits) >= 4:
                to_acc = f"Счет {get_mask_account(digits)}"
        else:
            digits = "".join(ch for ch in to_acc if ch.isdigit())
            if len(digits) == 16:
                name = "".join(
                    ch for ch in to_acc if ch.isalpha() or ch.isspace()
                ).strip()
                to_acc = f"{name} {get_mask_card_number(digits)}"

    # Собираем строку
    result = f"\n{date} {description}"
    if from_acc and to_acc:
        result += f"\n{from_acc} -> {to_acc}"
    result += f"\nСумма: {amount} {currency}\n"

    return result


def main():
    """Основная логика программы."""
    data = load_data()
    if not data:
        print("Нет данных")
        return

    # Фильтрация по статусу
    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    status = input("Введите статус: ").upper()
    while status not in ("EXECUTED", "CANCELED", "PENDING"):
        print(f'Статус "{status}" недоступен.')
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input("Введите статус: ").upper()

    # Фильтруем по статусу
    if "state" in data[0]:
        data = [t for t in data if t.get("state") == status]
    print(f'Операции отфильтрованы по статусу "{status}"')

    # Сортировка
    if input("Отсортировать по дате? Да/Нет: ").lower() == "да":
        order = input("По возрастанию или убыванию? ").lower()
        reverse = order == "убыванию"
        data.sort(key=lambda x: x.get("date", ""), reverse=reverse)

    # Фильтр по валюте
    if input("Выводить только рублевые транзакции? Да/Нет: ").lower() == "да":
        # Универсальная проверка для JSON и CSV
        filtered_data = []
        for t in data:
            if (
                    "operationAmount" in t
                    and t["operationAmount"]["currency"]["name"] == "руб."
            ):

                filtered_data.append(t)
            elif t.get("currency_name") == "Ruble":
                filtered_data.append(t)
        data = filtered_data

    # Поиск по описанию
    if input("Отфильтровать по слову в описании? Да/Нет: ").lower() == "да":
        search = input("Введите слово: ")
        data = process_bank_search(data, search)

    # Вывод
    print("Распечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(data)}")

    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        for t in data:
            print(format_transaction(t))


if __name__ == "__main__":
    main()
