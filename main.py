import re
from typing import Any, Dict, Iterator, List
from src.generators import transaction_descriptions
from src.handler import search_transactions
from src.processing import dicts_by_state, sort_dicts_by_date
from src.readCSVandXLSX import read_csv, read_file_from_file_xlsx

from src.utils import read_transaction_from_file_json, sum_amount
from src.widget import convert_datetime_to_date, masks_of_cards


def handle_file_selection() -> Any:
    """предлагает пользователю выбрать тип файла и возвращает обработанные данные."""
    file_type = input("Введите статус по которому необходимо выполнить фильтрацию: json, csv, xlsx \n").lower()

    if file_type == "1" or file_type == "json":
        print("Обрабатываю JSON-файл...")
        return read_transaction_from_file_json("data/operations.json")

    elif file_type == "2" or file_type == "csv":
        print("Обрабатываю CSV-файл...")
        return read_csv("data/transactions.csv")

    elif file_type == "3" or file_type == "xlsx":
        print("Обрабатываю файл Excel...")
        return read_file_from_file_xlsx("data/transactions_excel.xlsx")

    else:
        print("Неверный ввод. Пожалуйста, введите 1, 2 или 3.")


def handle_status_filtering(data: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:
    """Фильтрует транзакции на основе выбранного пользователем статуса."""
    status = input("Введите статус фильтрации (EXECUTED, CANCELED, PENDING выполнения): ").upper()
    if status.upper() not in ("EXECUTED", "CANCELED", "PENDING"):
        print("Статус не корректен, введите ешё раз")
        return handle_status_filtering(data)
    return dicts_by_state(data, status)


def handle_sort_by_date(data: List[Dict[Any, Any]]) -> List[Dict[Any, Any]] | Iterator[dict]:
    """Сортирует список транзакций"""
    sort = input("Отсортировать операции по дате? Да/Нет \n")
    if sort.lower() == "да":
        figure = input("по возрастанию/по убыванию \n")
        if figure.lower() == "по возрастанию":
            return sort_dicts_by_date(data)
        elif figure.lower() == "по убыванию":
            return sort_dicts_by_date(data, reverse=True)
        else:
            print("Не коректное значение, введите ещё раз")
            return sort_dicts_by_date(data)
    elif sort.lower() == "нет":
        return data
    else:
        print("Не корректный ответ, повторите ввод")
        return sort_dicts_by_date(data)


def handle_keyword_filtering(data: List[Dict[Any, Any]]) -> Any:
    """Фильтрует транзакции на основе введенного пользователем ключевого слова."""
    filter_choice = input("Фильтровать транзакции по ключевому слову в описании? (Да/Нет): ").lower()
    if filter_choice == "да":
        keyword = input("Введите ключевое слово: ")
        print(f"Фильтрация по ключевому слову: {keyword}")
        return search_transactions(data, keyword)
    elif filter_choice == "нет":
        print("Пропуск фильтрации по ключевым словам...")
        return data
    else:
        print("Неверный ввод. Пожалуйста, выберите 'Да' или 'Нет'.")


def print_formatted_transactions(data: List[Dict[Any, Any]]) -> None:
    """Печатает отформатированные сведения о транзакции."""

    print("Печать окончательного списка транзакций...")
    if data:
        descriptions_iterator = transaction_descriptions(data)
        for transaction in data:
            print(convert_datetime_to_date(transaction["date"]), next(descriptions_iterator))
            if re.search("Перевод", transaction["description"]):
                print(masks_of_cards(transaction["from"]), "->", masks_of_cards(transaction["to"]))
            else:
                print(masks_of_cards(transaction["to"]))
                print(f"Amount: {sum_amount(transaction)} RUB. \n")
    else:
        print("Не найдено транзакций, соответствующих вашим критериям фильтрации.")


def main() -> None:
    """Основная функция для запуска конвейера обработки транзакций."""
    print("Добро пожаловать в службу обработки банковских транзакций!")
    data = handle_file_selection()
    data = handle_status_filtering(data)
    data = handle_sort_by_date(data)
    data = handle_keyword_filtering(data)
    print_formatted_transactions(data)


if __name__ == "__main__":
    main()
