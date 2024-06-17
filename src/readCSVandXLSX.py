import os
import pandas as pd
from typing import Any


def read_csv(filename: str) -> Any:
    """Считывает CSV-файл и возвращает список словарей."""
    filename = os.path.abspath(filename)
    try:
        df = pd.read_csv(filename, encoding="utf-8")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден. Проверьте путь к файлу.")
        return []
    except Exception as e:
        print(f"Ошибка чтения CSV файла: {e}")
        return []


def read_xlsx(filename: str) -> Any:
    """Считывает CSV-файл и возвращает список словарей."""
    filename = os.path.abspath(filename)
    try:
        df = pd.read_csv(filename, encoding="utf-8")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден. Проверьте путь к файлу.")
        return []
    except Exception as e:
        print(f"Ошибка чтения CSV файла: {e}")
        return []


