import unittest
from typing import Any
from unittest.mock import patch

from pandas import DataFrame

from src.readCSVandXLSX import read_csv, read_xlsx


class TestCSVXLSXReader(unittest.TestCase):
    """Тесты для функций чтения CSV и XLSX файлов."""

    def test_read_csv(self) -> None:
        """Тест для функции read_csv."""
        file_path = "../data/transactions.csv"
        transactions = read_csv(file_path)
        self.assertIsInstance(transactions, list)
        self.assertTrue(all(isinstance(transaction, dict) for transaction in transactions))

    def test_read_csv_invalid_file(self) -> None:
        """Тест для read_csv с неверным типом файла."""
        file_path = "data.txt"
        transactions = read_csv(file_path)
        self.assertEqual(transactions, [])

    @patch("pandas.read_excel")
    def test_read_xlsx(self, mock_read_excel: Any) -> None:
        """Тестирование read_xlsx."""
        mock_data = [{"date": "2022-01-01", "amount": 100.00}, {"date": "2022-02-01", "amount": 200.00}]
        mock_read_excel.return_value = DataFrame(mock_data)
        result_xlsx = read_xlsx("../data/transactions_excel.xlsx")
        self.assertEqual(result_xlsx, mock_data)

    def test_read_xlsx_invalid_file(self) -> None:
        """Тест для read_xlsx с неверным типом файла."""
        file_path = "data.txt"
        transactions = read_xlsx(file_path)
        self.assertEqual(transactions, [])


if __name__ == "__main__":
    unittest.main()
