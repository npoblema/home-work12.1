import json
import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.logging import logger_setup

logger = logger_setup()


load_dotenv()
API_KEY = os.getenv("api_keys")


def get_currency_rate(currency: Any) -> Any:
    """Получает курс валюты от API и возвращает его в виде float"""
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY}, timeout=15)
    response_data = json.loads(response.text)
    rate = response_data["rates"]["RUB"]
    if rate:
        logging.info("Функция get_currency_rate выполнена успешно")
    else:
        logging.error("С функцией get_currency_rate что-то пошло не так: %(error)s")
    return rate
