import pytest
import pandas as pd
from unittest.mock import patch, Mock
from src.utils import read_transactions, get_greeting, get_currency_rates, get_stock_prices
from datetime import datetime
import logging


# Фикстура для тестового DataFrame
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "Дата операции": ["2025-05-10"],
        "Сумма операции": [1000.50],
        "Категория": ["Супермаркеты"]
    })


# Тесты для read_transactions
@patch("pandas.read_excel")
def test_read_transactions_success(mock_read_excel, sample_dataframe, tmp_path):
    # Подготовка
    file_path = tmp_path / "test.xlsx"
    mock_read_excel.return_value = sample_dataframe

    # Вызов
    result = read_transactions(str(file_path))

    # Проверки
    assert result.equals(sample_dataframe)
    mock_read_excel.assert_called_once_with(str(file_path))


@patch("pandas.read_excel")
def test_read_transactions_file_not_found(mock_read_excel):
    # Подготовка
    mock_read_excel.side_effect = FileNotFoundError("File not found")

    # Проверка
    with pytest.raises(FileNotFoundError, match="File not found"):
        read_transactions("nonexistent.xlsx")


@patch("src.utils.logging.info")
@patch("src.utils.logging.error")
def test_read_transactions_logging(mock_error, mock_info, sample_dataframe, tmp_path):
    # Подготовка
    file_path = tmp_path / "test.xlsx"
    with patch("pandas.read_excel", return_value=sample_dataframe):
        # Успешный вызов
        read_transactions(str(file_path))
        mock_info.assert_called_with(f"Successfully read transactions from {str(file_path)}")

    # Ошибка
    with patch("pandas.read_excel", side_effect=FileNotFoundError("File not found")):
        with pytest.raises(FileNotFoundError):
            read_transactions(str(file_path))
        mock_error.assert_called_with("Error reading transactions: File not found")


# Тесты для get_greeting
@pytest.mark.parametrize(
    "hour, expected_greeting",
    [
        (6, "Доброе утро"),  # 06:00
        (11, "Доброе утро"),  # 11:59
        (12, "Добрый день"),  # 12:00
        (17, "Добрый день"),  # 17:59
        (18, "Добрый вечер"),  # 18:00
        (23, "Добрый вечер"),  # 23:59
        (0, "Доброй ночи"),  # 00:00
        (5, "Доброй ночи"),  # 05:59
    ],
)
def test_get_greeting(hour, expected_greeting):
    dt = datetime(2025, 5, 14, hour, 0)
    result = get_greeting(dt)
    assert result == expected_greeting


# Тесты для get_currency_rates
@patch("src.utils.requests.get")
def test_get_currency_rates_success(mock_get):
    # Подготовка
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 73.21}}
    mock_get.return_value = mock_response

    # Вызов
    result = get_currency_rates(["USD"], "test_api_key")

    # Проверки
    assert result == [{"currency": "USD", "rate": 73.21}]
    mock_get.assert_called_once_with(
        "https://api.exchangerate-api.com/v4/latest/USD",
        params={"api_key": "test_api_key"}
    )


@patch("src.utils.requests.get")
def test_get_currency_rates_api_error(mock_get):
    # Подготовка
    mock_get.side_effect = Exception("API error")

    # Вызов
    result = get_currency_rates(["USD"], "test_api_key")

    # Проверки
    assert result == []  # Пустой список при ошибке


@patch("src.utils.logging.error")
def test_get_currency_rates_logging(mock_error):
    # Подготовка
    with patch("src.utils.requests.get", side_effect=Exception("API error")):
        # Вызов
        get_currency_rates(["USD"], "test_api_key")
        # Проверка
        mock_error.assert_called_with("Error fetching currency USD: API error")


# Тесты для get_stock_prices
@patch("src.utils.requests.get")
def test_get_stock_prices_success(mock_get):
    # Подготовка
    mock_response = Mock()
    mock_response.json.return_value = {"Global Quote": {"05. price": "150.12"}}
    mock_get.return_value = mock_response

    # Вызов
    result = get_stock_prices(["AAPL"], "test_api_key")

    # Проверки
    assert result == [{"stock": "AAPL", "price": 150.12}]
    mock_get.assert_called_once_with(
        "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=test_api_key"
    )


@patch("src.utils.requests.get")
def test_get_stock_prices_api_error(mock_get):
    # Подготовка
    mock_get.side_effect = Exception("API error")

    # Вызов
    result = get_stock_prices(["AAPL"], "test_api_key")

    # Проверки
    assert result == []  # Пустой список при ошибке


@patch("src.utils.logging.error")
def test_get_stock_prices_logging(mock_error):
    # Подготовка
    with patch("src.utils.requests.get", side_effect=Exception("API error")):
        # Вызов
        get_stock_prices(["AAPL"], "test_api_key")
        # Проверка
        mock_error.assert_called_with("Error fetching stock AAPL: API error")