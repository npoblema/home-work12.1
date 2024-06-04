from typing import List

import pandas as pd


def read_csv(filename: str) -> list:
    """Читает file scv и возвращает список"""
    if filename.endswith(".csv"):
        df = pd.read_csv(filename, encoding="utf-8")
        transactions = df.to_dict(orient="records")
        return transactions
    else:
        return []


def read_xlsx(filename: str) -> List:
    """Читает file xlsx и возвращает список"""
    if filename.endswith(".xlsx"):
        data = pd.read_excel(filename)
        return data.to_dict("records")
    else:
        return []


print(read_csv("../data/transactions.csv"))
print(read_xlsx("../data/transactions_excel.xlsx"))
# Проверка
