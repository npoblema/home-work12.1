import json
import os
from unittest.mock import Mock, patch

import pytest

from src.utils import convert_amount_to_rubles, load_transactions_from_json


@pytest.mark.parametrize(
    "value, expected",
    (([[{"key": "value"}], [{"key": "value"}]], [[{"key": "value"}], [{"key": "value"}]]), ([{}, []], [{}, []])),
)
@patch("builtins.open", create=True)
def test_convert_json_file(mock_open: Mock, value: list | dict, expected: list) -> None:
    mock_file = mock_open.return_value.__enter__.return_value
    mock_file.read.return_value = json.dumps(value)
    assert load_transactions_from_json(os.path.join("..", "data", "operations.json")) == expected
    mock_open.assert_called_once_with(os.path.join("..", "data", "operations.json"), "r", encoding="utf-8")


@patch("requests.get")
def test_calculate_transaction_amount(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {"conversion_rates": {"RUB": 52.99}}
    transaction = {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.20 6878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
    }
    expected_amount = 4192300.1407
    assert convert_amount_to_rubles(transaction) == expected_amount


def test_calculate_transaction_amount_rub() -> None:
    transaction = {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "RUB", "code": "RUB"}},
    }
    assert convert_amount_to_rubles(transaction) == 79114.93
