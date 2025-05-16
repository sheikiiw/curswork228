from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import (process_data, fetch_api_data, load_transactions_file,
                       parse_datetime_string)


def test_parse_datetime_valid():
    """Тест парсинга корректной строки даты."""
    date_string = "2024-01-01 12:00:00"
    parsed_datetime = parse_datetime_string(date_string)
    assert isinstance(parsed_datetime, datetime)
    assert parsed_datetime.year == 2024
    assert parsed_datetime.month == 1
    assert parsed_datetime.day == 1


def test_parse_datetime_invalid():
    """Тест парсинга некорректной строки даты."""
    with pytest.raises(ValueError):
        parse_datetime_string("invalid-date")


def test_fetch_api_data():
    """Тест получения данных с API."""
    request_date = datetime(2024, 1, 1)
    records = fetch_api_data(request_date)
    assert isinstance(records, list)
    assert all('value' in record and 'date' in record for record in records)


def test_process_data_valid():
    """Тест обработки корректных данных."""
    test_records = [
        {"value": 100, "date": "2024-01-01"},
        {"value": 200, "date": "2024-01-01"}
    ]
    result = process_data(test_records)
    assert result["average_value"] == 150
    assert result["records_count"] == 2


def test_process_data_missing_value_column():
    """Тест обработки данных без колонки 'value'."""
    test_records = [
        {"amount": 100, "date": "2024-01-01"}
    ]
    result = process_data(test_records)
    assert result["average_value"] is None
    assert result["records_count"] == 1


@patch('src.views.pd.read_excel')
def test_load_transactions_valid(mock_read_excel):
    """Тест успешной загрузки файла транзакций."""
    mock_dataframe = pd.DataFrame({
        "Дата операции": ["2024-01-01", "2024-01-02"]
    })
    mock_read_excel.return_value = mock_dataframe

    transactions_df = load_transactions_file("fake_path.xlsx")
    assert isinstance(transactions_df, pd.DataFrame)
    assert "Дата операции" in transactions_df.columns


@patch('src.views.pd.read_excel')
def test_load_transactions_missing_column(mock_read_excel):
    """Тест ошибки при отсутствии колонки 'Дата операции'."""
    mock_dataframe = pd.DataFrame({
        "Другой столбец": ["2024-01-01"]
    })
    mock_read_excel.return_value = mock_dataframe

    with pytest.raises(ValueError):
        load_transactions_file("fake_path.xlsx")
