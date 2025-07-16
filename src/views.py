import json
import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv

from src.utils import filter_by_date, get_currency_rates, get_stock_prices, reading_xlsx

load_dotenv()


def get_greeting(date_str: str) -> str:
    """Определяет и возвращает приветствие в зависимости от времени суток."""
    time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").time()
    if 5 <= time.hour < 12:
        return "Доброе утро"
    elif 12 <= time.hour < 17:
        return "Добрый день"
    elif 17 <= time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_stats(df) -> list[dict]:
    """
    Создает сводку по картам пользователя:
     показывает общую сумму потраченного и размер кэшбека
    """
    grouped = df.groupby("Номер карты")["Сумма платежа"].sum().reset_index()

    result = []
    for column, row in grouped.iterrows():
        last_digits = str(row["Номер карты"])
        total_spent = round(row["Сумма платежа"], 2)
        cashback = round(total_spent / 100, 2)

        result.append({"last_digits": last_digits, "total_spent": total_spent, "cashback": cashback})

    return result


def get_top_transactions(df, tran_top=5) -> list[dict]:
    """Возвращает топ-5 транзакций по убыванию суммы платежа."""
    df_sorted = df.sort_values(by="Сумма платежа", ascending=False).head(tran_top)

    result = []
    for _, row in df_sorted.iterrows():
        result.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": round(row["Сумма платежа"], 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    return result


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(CURRENT_DIR, "..", "user_settings.json")
DATA_PATH = os.path.join(CURRENT_DIR, "..", "data", "operations.xlsx")


def main_view(input_date: str, file_path: str = DATA_PATH, settings_path: str = SETTINGS_PATH) -> dict[str, Any]:
    """ Основной обработчик данных: формирует главную страницу с различными аналитическими блоками.
    Собирает всю необходимую информацию о картах, последних операциях, курсах валют и акциях.
    :param input_date: Дата анализа (до которой фильтруются данные)
    :param file_path: Путь к файлу с операциями
    :param settings_path: Путь к файлу с настройками пользователя
    :return: Словарь с итоговыми результатами для главной страницы """
    df = reading_xlsx(file_path)
    filtered_df = filter_by_date(df, input_date)
    greeting = get_greeting(input_date)

    cards = get_card_stats(filtered_df)
    top_tx = get_top_transactions(filtered_df)

    with open(settings_path, encoding="utf-8") as f:
        settings = json.load(f)
        print(settings)

    currencies = settings.get("user_currencies", [])
    stocks = settings.get("user_stocks", [])

    currency_rates = get_currency_rates(currencies)
    stock_prices = get_stock_prices(stocks)

    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_tx,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
