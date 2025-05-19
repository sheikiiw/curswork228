from unittest.mock import patch

import pandas as pd
import pytest

from src.views import home_page


@pytest.fixture
def sample_transactions():
    return pd.DataFrame({
        "Дата операции": ["2025-05-10", "2025-05-11"],
        "Номер карты": ["*1234", "*5678"],
        "Сумма платежа": [1000, 500],
        "Категория": ["Супермаркеты", "Фастфуд"],
        "Описание": ["Покупка", "Еда"]
    })


@patch("src.views.read_transactions")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_home_page(mock_stocks, mock_currencies, mock_read, sample_transactions):
    mock_read.return_value = sample_transactions
    mock_currencies.return_value = [{"currency": "USD", "rate": 73.21}]
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150.12}]

    result = home_page("2025-05-14 14:00:00")

    assert result["greeting"] == "Добрый день"
    assert len(result["cards"]) == 2
    assert result["cards"][0]["last_digits"] == "1234"
    assert result["cards"][0]["total_spent"] == 1000
    assert result["cards"][0]["cashback"] == 10
