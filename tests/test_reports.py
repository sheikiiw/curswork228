import pytest
import pandas as pd
from unittest.mock import patch, Mock
from src.reports import spending_by_category
from datetime import datetime, timedelta
import json
import os


# Фикстура для тестового DataFrame
@pytest.fixture
def sample_transactions():
    return pd.DataFrame({
        "Дата операции": [
            "2025-05-10",
            "2025-04-15",
            "2025-03-01",
            "2025-02-01",  # За пределами 3 месяцев
            "2025-05-11",
        ],
        "Категория": [
            "Супермаркеты",
            "Супермаркеты",
            "Фастфуд",
            "Супермаркеты",
            "Супермаркеты",
        ],
        "Сумма платежа": [
            1000.50,
            500.25,
            200.00,
            300.00,
            600.75,
        ],
    })


# Проверка корректного расчета трат
def test_spending_by_category_correct_calculation(sample_transactions):
    result = spending_by_category(sample_transactions, "Супермаркеты", "2025-05-15")
    assert result["category"] == "Супермаркеты"
    assert result["total_spent"] == 2101.50  # 1000.50 + 500.25 + 600.75
    assert result["period"] == "2025-02-15 to 2025-05-15"


# Проверка при отсутствии категории
def test_spending_by_category_no_transactions(sample_transactions):
    result = spending_by_category(sample_transactions, "Транспорт", "2025-05-15")
    assert result["category"] == "Транспорт"
    assert result["total_spent"] == 0.0
    assert result["period"] == "2025-02-15 to 2025-05-15"


# Проверка без указания даты
@patch("src.reports.datetime")
def test_spending_by_category_no_date(mock_datetime, sample_transactions):
    mock_datetime.now.return_value = datetime(2025, 5, 15)
    result = spending_by_category(sample_transactions, "Супермаркеты")
    assert result["total_spent"] == 2101.50
    assert result["period"] == "2025-02-15 to 2025-05-15"


# Проверка неверного формата даты
def test_spending_by_category_invalid_date(sample_transactions):
    with pytest.raises(ValueError, match="Date must be in format YYYY-MM-DD"):
        spending_by_category(sample_transactions, "Супермаркеты", "2025-13-15")


# Проверка работы декоратора
@patch("src.reports.json.dump")
@patch("builtins.open", new_callable=pytest.mock_open)
def test_spending_by_category_decorator(mock_open, mock_json_dump, sample_transactions):
    spending_by_category(sample_transactions, "Супермаркеты", "2025-05-15")
    mock_open.assert_called_once()
    mock_json_dump.assert_called_once()


# Проверка логирования
@patch("src.reports.logging.info")
@patch("src.reports.logging.error")
def test_spending_by_category_logging(mock_error, mock_info, sample_transactions):
    # Успешный вызов
    spending_by_category(sample_transactions, "Супермаркеты", "2025-05-15")
    mock_info.assert_called_with("Calculating spending for category Супермаркеты")

    # Вызов с ошибкой
    with pytest.raises(ValueError):
        spending_by_category(sample_transactions, "Супермаркеты", "2025-13-15")
    mock_error.assert_called_with("Invalid date format")