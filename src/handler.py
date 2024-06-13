import os
import json
import re
from collections import defaultdict
from typing import Any, Dict, List


def search_transactions(all_transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Функция проверяющая наличие строки поиска в описании"""
    matching_transactions = []
    for transaction in all_transactions:
        if "description" in transaction and re.search(search_string, transaction["description"], re.IGNORECASE):
            matching_transactions.append(transaction)
    return matching_transactions


def categorize_transactions(transactions: List[Dict[str, Any]], categories: Dict[str, List[str]]) -> Dict[str, int]:
    """Подсчет операции в каждой категории"""
    category_counts = defaultdict(int)
    for transaction in transactions:
        if "description" in transaction:
            for category, keywords in categories.items():
                if any(keyword.lower() in transaction["description"].lower() for keyword in keywords):
                    category_counts[category] += 1
                    break
    return category_counts


def read_transactions_from_json(filename: str) -> List[Dict[str, Any]]:
    """Чтение транзакций из json файла"""
    absolute_path = os.path.abspath(filename)
    with open(absolute_path, "r", encoding="utf-8") as file:
        return json.load(file)


all_transactions = read_transactions_from_json("../data/operations.json")

categories = {"Перевод": ["Перевод организации", "Перевод частному лицу"]}

category_counts = categorize_transactions(all_transactions, categories)

test_transactions = [
    {"description": "Оплата за интернет"},
    {"description": "Покупка продуктов в магазине"},
    {"description": "Перевод денег другу"},
    {"description": "Оплата за мобильную связь"},
    {"description": "Покупка билетов на концерт"},
]

test_categories = {
    "Интернет": ["интернет", "онлайн"],
    "Продукты": ["продукты", "магазин"],
    "Другое": ["перевод", "концерт", "билеты"],
}

result = categorize_transactions(test_transactions, test_categories)
print(result)
