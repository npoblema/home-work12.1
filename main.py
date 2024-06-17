import re
from typing import Any, Dict, Iterator, List, Type

from src.readCSVandXLSX import read_csv, read_xlsx
from src.generators import transaction_descriptions
from src.handler import search_transactions
from src.processing import sort_dicts_by_date
from src.utils import load_transactions_from_json, convert_amount_to_rubles
from src.widget import convert_datetime_to_date, masks_of_cards


def handle_file_selection() -> Any:
    """предлагает пользователю выбрать тип файла и возвращает обработанные данные."""

    while True:
        file_type = input("Введите статус по которому необходимо выполнить фильтрацию: json, csv, xlsx"
                          ).lower()

        if file_type == "1" or file_type == "json":
            print("Обрабатываю JSON-файл...")
            return load_transactions_from_json("C:\\Users\\Student\\PycharmProjects\\skypro\\data\\operations.json")

        elif file_type == "2" or file_type == "csv":
            print("Обрабатываю CSV-файл...")
            return read_csv("C:\\Users\\Student\\PycharmProjects\\skypro\\data\\transactions.csv")

        elif file_type == "3" or file_type == "xlsx":
            print("Обрабатываю файл Excel...")
            return read_xlsx("C:\\Users\\Student\\PycharmProjects\\skypro\\data\\transactions_excel.xlsx")

        else:
            print("Неверный ввод. Пожалуйста, введите 1, 2 или 3.")


def handle_status_filtering(data: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:
    """Фильтрует транзакции на основе выбранного пользователем статуса."""

    while True:
        status = input("Введите статус фильтрации (EXECUTED, CANCELED, PENDING выполнения).: ").upper()
        if status in ("EXECUTED", "CANCELED", "PENDING"):
            print(f"Фильтрация транзакций по статусу: {status}")
            return sort_dicts_by_date(data, Type[str])
        else:
            print("Статус недействителен. Пожалуйста, выберите правильный вариант.")


def handle_date_sorting(data: List[Dict[Any, Any]]) -> List[Dict[Any, Any]] | Iterator[dict]:
    """Сортировка транзакций по дате в зависимости от предпочтений пользователя."""

    while True:
        sort_choice = input("Сортировать транзакции по дате? (Да/Нет): ").lower()
        if sort_choice == "yes":
            while True:
                sort_order = input("Порядок сортировки (по возрастанию/убыванию): ").lower()
                if sort_order == "возрастанию":
                    print("Сортировка в порядке возрастания... ")
                    return sort_dicts_by_date(data)
                elif sort_order == "убыванию":
                    print("Сортировка в порядке убывания...")
                    return sort_dicts_by_date(data, reverse=True)
                else:
                    print("Недопустимый порядок сортировки. Пожалуйста, выберите 'По возрастанию' или 'По убыванию'.")
        elif sort_choice == "нет":
            print("Пропуск сортировки...")
            return data
        else:
            print("Неверный ввод. Пожалуйста, выберите 'Да' или 'Нет''.")


def handle_keyword_filtering(data: List[Dict[Any, Any]]) -> Any:
    """Фильтрует транзакции на основе введенного пользователем ключевого слова."""

    while True:
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
            print(convert_datetime_to_date(transaction["дата"]), next(descriptions_iterator))
            if re.search("Перевод", transaction["описание"]):
                print(masks_of_cards(transaction["от"]), "->", masks_of_cards(transaction["к"]))
            else:
                print(masks_of_cards(transaction["к"]))
                print(f"Amount: {convert_amount_to_rubles(transaction)} RUB\n")
    else:
        print("Не найдено транзакций, соответствующих вашим критериям фильтрации.")


def main() -> None:
    """Основная функция для запуска конвейера обработки транзакций."""
    print("Добро пожаловать в службу обработки банковских транзакций!")
    data = handle_file_selection()
    data = handle_status_filtering(data)
    data = handle_date_sorting(data)
    data = handle_keyword_filtering(data)
    print_formatted_transactions(data)


if __name__ == "__main__":
    main()
