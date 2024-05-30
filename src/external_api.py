import os

import requests
from dotenv import load_dotenv

from src.logging import logger_setup

logger = logger_setup()


load_dotenv()
API_KEY = os.getenv("api_keys")


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
        logger.info("Функция успешно выполнена!")
        return float(amount * rub_rate)
    except requests.exceptions.RequestException as e:
        logger.error("С функцией что-то не так!")
        print(f"Ошибка при получении курса: {e}")
        return 0.0
