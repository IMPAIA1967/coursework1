import os

import finnhub
import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()


def reading_xlsx(file_path: str) -> DataFrame:
    """ Читает Excel-файл и преобразует его в объект Pandas DataFrame. """
    df = pd.read_excel(file_path)
    return df


def filter_by_date(df: DataFrame, end_date_str: str) -> pd.DataFrame:
    """ Возвращает набор данных за период с первого числа указанного месяца
     до конца заданной даты включительно. """
    df = df.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    end_date = pd.to_datetime(end_date_str)

    start_date = end_date.replace(day=1)
    return df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]


def get_currency_rates(symbols: list[str], base: str = "RUB") -> list[dict]:
    """ Получает актуальные обменные курсы валют, указанные в списке `symbols`,
     конвертируя их в базовую валюту RUB, используя API apilayer. """
    api_key = os.getenv("API_KEY_LAYER")  # читаем ключ
    if not api_key:
        raise ValueError("Переменная окружения API_KEY_LAYER не установлена")

    result_list = []
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={base}&symbols={','.join(symbols)}"
    headers = {"apikey": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка при получении курса валют: {response.status_code}, {response.text}")
        return []

    json_response = response.json()
    rates = json_response.get("rates", {})

    for symbol in symbols:
        rate = rates.get(symbol)
        if rate:
            result_list.append({"currency": symbol, "rate": round(float(rate), 2)})

    return result_list


if __name__ == "__main__":
    print(get_currency_rates(["EUR", "USD"]))
    # [{'currency': 'EUR', 'rate': 91.210065}, {'currency': 'USD', 'rate': 78.021461}]


def get_stock_prices(stocks: list[str]) -> list[dict]:
    """ Получает текущие котировки акций,
    указанных в списке `stocks`, используя API FinHub. """
    finnhub_key = os.getenv("FINNHUB_API_KEY")

    client = finnhub.Client(api_key=finnhub_key)
    results = []

    for stock in stocks:
        try:
            quote = client.quote(stock)
            price = quote.get("c")  # текущая цена
            if price:
                results.append({"stock": stock, "price": round(price, 2)})
        except Exception as e:
            results.append({"stock": stock, "price": 0.0})
            print(f"Ошибка при получении цены для {stock}: {e}")

    return results
