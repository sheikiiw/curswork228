from typing import Any, Dict, List
from unittest.mock import patch

import pytest

from src.services import investment_bank


# Фикстура для тестовых транзакций
@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {
            "Дата операции": "2025-05-10",
            "Сумма операции": 1712.50,
        },
        {
            "Дата операции": "2025-05-11",
            "Сумма операции": 123.75,
        },
        {
            "Дата операции": "2025-04-30",  # Другой месяц
            "Сумма операции": 500.00,
        },
    ]


# Проверка корректного расчета для разных лимитов
@pytest.mark.parametrize(
    "limit, expected_saved",
    [
        (10, 13.75),  # 1712.50 -> 1713 (0.50), 123.75 -> 124 (0.25), 0.50 + 0.25 = 0.75
        (50, 63.75),  # 1712.50 -> 1750 (37.50), 123.75 -> 150 (26.25), 37.50 + 26.25 = 63.75
        (100, 163.75),  # 1712.50 -> 1800 (87.50), 123.75 -> 200 (76.25), 87.50 + 76.25 = 163.75
    ],
)
def test_investment_bank_correct_calculation(sample_transactions, limit, expected_saved):
    result = investment_bank("2025-05", sample_transactions, limit)
    assert result["total_saved"] == expected_saved


# Проверка пустого списка транзакций
def test_investment_bank_empty_transactions():
    result = investment_bank("2025-05", [], 50)
    assert result["total_saved"] == 0.0


# Проверка транзакций за другой месяц
def test_investment_bank_no_matching_month(sample_transactions):
    result = investment_bank("2025-06", sample_transactions, 50)
    assert result["total_saved"] == 0.0


# Проверка неверного формата месяца
def test_investment_bank_invalid_month(sample_transactions):
    with pytest.raises(ValueError, match="Month must be in format YYYY-MM"):
        investment_bank("2025-13", sample_transactions, 50)


# Проверка неверного лимита
def test_investment_bank_invalid_limit(sample_transactions):
    with pytest.raises(ValueError, match="Limit must be 10, 50, or 100"):
        investment_bank("2025-05", sample_transactions, 25)


# Проверка логирования
@patch("src.services.logging.info")
@patch("src.services.logging.error")
def test_investment_bank_logging(mock_error, mock_info, sample_transactions):
    # Успешный вызов
    investment_bank("2025-05", sample_transactions, 50)
    mock_info.assert_called_with("Calculating Investment Bank for 2025-05 with limit 50")

    # Вызов с ошибкой
    with pytest.raises(ValueError):
        investment_bank("2025-13", sample_transactions, 50)
    mock_error.assert_called_with("Invalid month format")
