import json
import os
from typing import Dict
from src.logging import logger_setup

import requests
from dotenv import load_dotenv

logger = logger_setup()

load_dotenv()
API_KEY = os.getenv("API_KEY")


def load_transactions_from_json(file_path: str) -> list[dict]:
    """
    Загружает транзакции из JSON-файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.info("Функция работает успешно!")
                return data
            else:
                logger.error("С функцией что-то не так!")
                return []
    except FileNotFoundError:
        logger.error("Ошибка FileNotFoundError")
        return []
    except json.decoder.JSONDecodeError:
        logger.error("Ошибка чтения файла json")
        return []


def convert_amount_to_rubles(transaction: Dict) -> float:
    """
    Преобразует сумму транзакции в рубли (RUB).
    """
    currency_code = transaction["operationAmount"]["currency"]["code"]
    amount = float(transaction["operationAmount"]["amount"])

    if currency_code == "RUB":
        logger.info("Функция работает успешно!")
        return amount
    else:
        logger.error("С функцией что-то не так!")
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
        logger.info("Функция работает успешно!")
        return float(amount * rub_rate)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении курса: {e}")
        logger.error("С функцией что-то не так!")
        return 0.0


value = {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
        "amount": "31957.58",
        "currency": {
            "name": "руб.",
            "code": "RUB"
        }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
}
convert_amount_to_rubles(value)
