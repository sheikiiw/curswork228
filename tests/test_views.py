import json
from unittest.mock import mock_open, patch

import pandas as pd

from src.views import home_page  # Убедись, что путь корректен

# Подготовка фейковых данных
mock_settings = {
    "user_currencies": ["USD", "EUR"],
    "user_stocks": ["AAPL", "TSLA"]
}

mock_transactions = pd.DataFrame([
    {
        "Дата операции": "14.05.2025 13:30:00",
        "Номер карты": "1234567812345678",
        "Сумма платежа": 500.0,
        "Категория": "Супермаркеты",
        "Описание": "Покупка еды"
    },
    {
        "Дата операции": "10.05.2025 10:00:00",
        "Номер карты": "1234567812345678",
        "Сумма платежа": 300.0,
        "Категория": "АЗС",
        "Описание": "Бензин"
    },
])


@patch("src.views.read_transactions")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
@patch("src.views.get_greeting")
@patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_settings))
def test_home_page(mock_file, mock_greeting, mock_stocks, mock_rates, mock_read_tx):
    mock_greeting.return_value = "Добрый день"
    mock_rates.return_value = [{"USD": 90.0}, {"EUR": 97.0}]
    mock_stocks.return_value = [{"AAPL": 180.0}, {"TSLA": 700.0}]
    mock_read_tx.return_value = mock_transactions

    result = home_page("2025-05-14 14:00:00")

    assert result["greeting"] == "Добрый день"
    assert len(result["cards"]) == 1
    assert result["cards"][0]["last_digits"] == "5678"
    assert result["cards"][0]["total_spent"] == 800.0
    assert result["cards"][0]["cashback"] == 8.0

    assert len(result["top_transactions"]) == 2
    assert result["top_transactions"][0]["Сумма платежа"] == 500.0
    assert result["currency_rates"] == [{"USD": 90.0}, {"EUR": 97.0}]
    assert result["stock_prices"] == [{"AAPL": 180.0}, {"TSLA": 700.0}]
