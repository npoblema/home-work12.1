import json
from collections import Counter
from typing import Any, Dict, List

import pandas as pd


def read_json_file(filename: str) -> Any:
    """Считывает файл JSON и возвращает список словарей."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден. Проверьте путь к файлу.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON файла '{filename}'.")
        return []
    except Exception as e:
        print(f"Ошибка чтения JSON файла: {e}")
        return []


def read_csv_file(filename: str) -> Any:
    """Считывает CSV-файл и возвращает список словарей."""
    try:
        df = pd.read_csv(filename)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден. Проверьте путь к файлу.")
        return []
    except Exception as e:
        print(f"Ошибка чтения CSV файла: {e}")
        return []


def read_excel_file(filename: str) -> Any:
    """Считывает файл Excel и возвращает список словарей."""
    try:
        df = pd.read_excel(filename)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден. Проверьте путь к файлу.")
        return []
    except Exception as e:
        print(f"Ошибка чтения Excel файла: {e}")
        return []


def filter_transactions_by_status(transactions: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрует список транзакций по статусу."""
    return [
        transaction
        for transaction in transactions
        if "status" in transaction and transaction["status"].upper() == status.upper()
    ]


def sort_transactions_by_date(transactions: List[Dict[str, Any]], order: str) -> List[Dict[str, Any]]:
    """Сортирует список транзакций по дате."""
    if order.lower() == "по возрастанию":
        return sorted(transactions, key=lambda x: x["date"])
    elif order.lower() == "по убыванию":
        return sorted(transactions, key=lambda x: x["date"], reverse=True)
    else:
        return transactions


def filter_transactions_by_word(transactions: List[Dict[str, Any]], word: str) -> List[Dict[str, Any]]:
    """Фильтрует список транзакций по слову в описании."""
    return [transaction for transaction in transactions if word.lower() in transaction["description"].lower()]


def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: Dict[str, str]) -> Dict[str, int]:
    """Подсчитывает количество транзакций в каждой категории."""
    transaction_categories = [categories[transaction["category"]] for transaction in transactions]
    return dict(Counter(transaction_categories))


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Печатает список транзакций."""
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for i, transaction in enumerate(transactions):
        print(f"{i + 1}. {transaction['date']} {transaction['description']}")
        print(f"Счет: {transaction['account']}")
        print(f"Сумма: {transaction['amount']} {transaction['currency']}")
        print()


def main() -> None:
    """Основная функция."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакициями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из json файла")
    print("2. Получить информацию о транзакциях из csv файла")
    print("3. Получить информацию о транзакциях из xlsx файла")

    choice = input("Введите номер пункта меню: ")

    if choice == "1":
        transactions = read_json_file("C:/Users/Student/PycharmProjects/skypro/data/operations.json")
        print("Для обработки выбран json файл.")
    elif choice == "2":
        transactions = read_csv_file("C:/Users/Student/PycharmProjects/skypro/data/transactions.csv")
        print("Для обработки выбран csv файл.")
    elif choice == "3":
        transactions = read_excel_file("C:/Users/Student/PycharmProjects/skypro/data/transactions_excel.xlsx")
        print("Для обработки выбран excel файл.")
    else:
        print("Неверный ввод. Пожалуйста, выберите пункт меню 1, 2 или 3.")
        return

    while True:
        status = input(
            "Введите статус по которому необходимо выполнить фильтрацию. Доступные для фильтровки статусы: "
            "EXECUTED, CANCELED, PENDING\n"
        )
        if status.upper() in ["EXECUTED", "CANCELED", "PENDING"]:
            transactions = filter_transactions_by_status(transactions, status)
            print(f"Операции отфильтрованы по статусу '{status.upper()}'")
            break
        else:
            print(f"Статус операции '{status}' недоступен.")

    while True:
        sort_by_date = input("Отсортировать операции по дате? Да/Нет\n")
        if sort_by_date.lower() == "да":
            order = input("Отсортировать по возрастанию или по убыванию?\n")
            transactions = sort_transactions_by_date(transactions, order)
            break
        elif sort_by_date.lower() == "нет":
            break
        else:
            print("Неверный ввод. Введите 'Да' или 'Нет'.")

    while True:
        filter_by_word = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n")
        if filter_by_word.lower() == "да":
            word = input("Введите слово для фильтрации:\n")
            transactions = filter_transactions_by_word(transactions, word)
            break
        elif filter_by_word.lower() == "нет":
            break
        else:
            print("Неверный ввод. Введите 'Да' или 'Нет'.")

    while True:
        filter_by_ruble = input("Выводить только рублевые транзакции? Да/Нет\n")
        if filter_by_ruble.lower() == "да":
            transactions = [transaction for transaction in transactions if transaction["currency"].lower() == "rub"]
            break
        elif filter_by_ruble.lower() == "нет":
            break
        else:
            print("Неверный ввод. Введите 'Да' или 'Нет'.")

    if transactions:
        print_transactions(transactions)
    else:
        print("Не найдено ни одной транзакции подходящей под ваши условия фильтрации")


if __name__ == "__main__":
    main()
