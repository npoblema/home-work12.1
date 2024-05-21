import json
import os
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def load_transactions_from_json(file_path: str) -> List[Dict]:
    """
    Загружает транзакции из JSON-файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except FileNotFoundError:
        return []
    except json.decoder.JSONDecodeError:
        return []


def convert_amount_to_rubles(transaction: Dict) -> float:
    """
    Преобразует сумму транзакции в рубли (RUB).
    """
    currency_code = transaction["operationAmount"]["currency"]["code"]
    amount = float(transaction["operationAmount"]["amount"])

    if currency_code == "RUB":
        return amount
    else:
        return get_currency_exchange_rate(currency_code, amount)


def get_currency_exchange_rate(from_currency: str, amount: float) -> float:
    """
    Получает обменный курс валюты к рублям (RUB) с помощью API.
    """
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rub_rate = data["conversion_rates"]["RUB"]
        return float(amount * rub_rate)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении курса: {e}")
        return 0.0
