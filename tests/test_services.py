import json
from unittest.mock import patch

import pandas as pd

from src.services import load_transactions_file, search_transactions


@patch("pandas.read_excel")
def test_load_transactions_success(mock_read_excel):
    """Тест успешной загрузки данных транзакций."""
    mock_dataframe = pd.DataFrame({"Дата операции": ["2024-01-01"], "Сумма": [100]})
    mock_read_excel.return_value = mock_dataframe

    transactions_df = load_transactions_file("fake_path.xlsx")
    assert isinstance(transactions_df, pd.DataFrame)
    assert len(transactions_df) == 1


@patch("src.services.load_transactions_file")
def test_search_transactions_found(mock_load_transactions):
    """Тест поиска с найденными результатами."""
    test_dataframe = pd.DataFrame({
        "Дата операции": ["2024-01-01", "2024-01-02"],
        "Описание": ["Покупка кофе", "Покупка книг"]
    })
    mock_load_transactions.return_value = test_dataframe

    result_json = search_transactions("кофе", "fake_path.xlsx")
    result = json.loads(result_json)

    assert "results_count" in result
    assert result["results_count"] == 1
    assert result["results"][0]["Описание"] == "Покупка кофе"


@patch("src.services.load_transactions_file")
def test_search_transactions_error(mock_load_transactions):
    """Тест поиска с ошибкой загрузки данных."""
    mock_load_transactions.side_effect = Exception("[Errno 2] No such file or directory: 'fake_path.xlsx'")

    result_json = search_transactions("что-то", "fake_path.xlsx")
    result = json.loads(result_json)

    assert "ошибка" in result
    assert "[Errno 2] No such file or directory" in result["ошибка"]
