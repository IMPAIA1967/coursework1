import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Optional

import pandas as pd

# Настройка логирования в файл logs/activity.log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/app.log", encoding="utf-8"), logging.StreamHandler()],
)


def save_report(func: Optional[Callable] = None, *, filename: Optional[str] = None):
    """ Декоратор для автоматического сохранения результатов отчёта в JSON-файл.
    Сохраняет отчёт только в том случае, если передан аргумент `save_to_file=True`."""

    def decorator(inner_func):
        @wraps(inner_func)
        def wrapper(*args, **kwargs):
            result = inner_func(*args, **kwargs)
            if kwargs.get("save_to_file"):
                report_filename = filename or f"logs/report_{inner_func.__name__}.json"
                try:
                    with open(report_filename, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                    logging.info(f"Отчет сохранен в файл: {report_filename}")
                except Exception as e:
                    logging.error(f"Не удалось сохранить отчет: {e}")
            return result

        return wrapper

    if callable(func):
        return decorator(func)
    return decorator


@save_report
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None, save_to_file: bool = False
) -> list[dict]:
    """ Возврат списка трат по выбранной категории за
    последние три месяца относительно указанной даты.
    По умолчанию используются текущая дата и сохранение отчёта отключено. """
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")

    start_date = end_date - timedelta(days=90)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce", dayfirst=True)
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    filtered = df[df["Категория"].astype(str).str.lower() == category.lower()]
    expenses = filtered[filtered["Сумма платежа"] < 0]

    result = [
        {
            "date": row["Дата операции"].strftime("%d.%m.%Y"),
            "amount": round(row["Сумма платежа"], 2),
            "description": row.get("Описание", ""),
        }
        for column, row in expenses.iterrows()
    ]
    logging.info(f"Найдено {len(result)} трат по категории '{category}' за 3 месяца")
    return result
