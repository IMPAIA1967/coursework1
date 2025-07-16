import os
from unittest.mock import MagicMock, patch

import pandas as pd

from src.utils import filter_by_date, get_currency_rates, get_stock_prices, reading_xlsx


@patch("pandas.read_excel")
def test_reading_xlsx(mock_get):
    mock_get.return_value = [
        {
            "Дата операции": "2021-12-10",
            "Сумма операции": -1000.0,
            "Категория": "Супермаркеты",
            "Описание": "Пятёрочка",
        }
    ]
    assert reading_xlsx("") == [
        {
            "Дата операции": "2021-12-10",
            "Сумма операции": -1000.0,
            "Категория": "Супермаркеты",
            "Описание": "Пятёрочка",
        }
    ]


def test_filter_by_date():
    """
    Проверяет фильтрацию по дате: данные с начала месяца до указанной даты.
    """
    df = pd.DataFrame(
        {
            "Дата операции": ["01.12.2021", "15.12.2021", "31.12.2021", "01.01.2022"],
            "Сумма платежа": [100, 200, 300, 400],
        }
    )
    result = filter_by_date(df, "2021-12-31")
    assert len(result) == 3
    assert result["Сумма платежа"].sum() == 600


def test_get_currency_rates():
    """Тест на получение курса валют"""
    with patch("requests.get") as mock_get:
        # Эмулируем успешный ответ API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"USD": 75.5}}
        mock_get.return_value = mock_response

        result = get_currency_rates(["USD"], "RUB")
        assert result == [{"currency": "USD", "rate": 75.5}]


def test_get_stock_prices_normal():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"c": 210.16}
        result = get_stock_prices(["AAPL"])
        assert result == [{"stock": "AAPL", "price": 210.16}]


def test_get_stock_prices_clear():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {}
        result = get_stock_prices([])
        assert result == []


def test_get_stock_prices_exc():
    # Установим поддельный ключ API
    fake_api_key = "FAKE_API_KEY"
    os.environ["FINNHUB_API_KEY"] = fake_api_key

    # Применим патч к клиенту finnhub.Client
    with patch("finnhub.Client") as MockFinnhubClient:
        # Эмулируем ошибку при запросе к API
        mock_client = MockFinnhubClient.return_value
        mock_client.quote.side_effect = Exception

        # Проверим реакцию функции на ошибку
        result = get_stock_prices(["AAPL"])
        expected_result = [{"stock": "AAPL", "price": 0.0}]
        assert result == expected_result
