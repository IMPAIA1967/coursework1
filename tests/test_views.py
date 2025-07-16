import os
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import DATA_PATH, get_card_stats, get_greeting, get_top_transactions, main_view


def test_get_greeting():
    assert get_greeting("2021-12-31 06:30:00") == "Доброе утро"
    assert get_greeting("2021-12-31 13:00:00") == "Добрый день"
    assert get_greeting("2021-12-31 19:30:00") == "Добрый вечер"
    assert get_greeting("2021-12-31 02:00:00") == "Доброй ночи"


def test_get_card_stats():
    data = {"Номер карты": ["*1111", "*1111", "*2222"], "Сумма платежа": [100.0, 200.0, 300.0]}
    df = pd.DataFrame(data)
    result = get_card_stats(df)

    assert len(result) == 2
    assert any(card["last_digits"] == "*1111" and card["total_spent"] == 300.0 for card in result)
    assert any(card["last_digits"] == "*2222" and card["cashback"] == 3.0 for card in result)


def test_get_top_transactions():
    data = {
        "Дата операции": [datetime(2021, 12, 30), datetime(2021, 12, 31)],
        "Сумма платежа": [1000.0, 500.0],
        "Категория": ["Пополнения", "Супермаркеты"],
        "Описание": ["Через банк", "Пятёрочка"],
    }
    df = pd.DataFrame(data)
    result = get_top_transactions(df, tran_top=1)

    assert len(result) == 1
    assert result[0]["amount"] == 1000.0
    assert result[0]["category"] == "Пополнения"


TEST_FILE = DATA_PATH


@pytest.mark.skipif(not os.path.exists(TEST_FILE), reason="Файл data/operations.xlsx не найден")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_main_view_output(mock_stocks, mock_currencies):
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150.0}, {"stock": "GOOGL", "price": 2500.0}]
    mock_currencies.return_value = [{"currency": "USD", "rate": 78.021461}, {"currency": "EUR", "rate": 91.210062}]

    result = main_view("2021-12-31 16:00:00", file_path=TEST_FILE)

    assert isinstance(result, dict)
    assert isinstance(result["greeting"], str)
    assert isinstance(result["cards"], list)
    assert isinstance(result["top_transactions"], list)
