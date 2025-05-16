from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import load_transactions_file


@patch('pandas.read_excel')
def test_load_transactions_success(mock_read_excel):
    """Тест успешной загрузки данных транзакций."""
    mock_dataframe = pd.DataFrame({
        "Дата операции": ["2024-01-01", "2024-01-02"]
    })
    mock_read_excel.return_value = mock_dataframe

    transactions_df = load_transactions_file("fake_path.xlsx")
    assert isinstance(transactions_df, pd.DataFrame)
    assert "Дата операции" in transactions_df.columns


@patch('pandas.read_excel')
def test_load_transactions_missing_column(mock_read_excel):
    """Тест ошибки при отсутствии ожидаемой колонки."""
    mock_dataframe = pd.DataFrame({
        "Другое поле": ["2024-01-01"]
    })
    mock_read_excel.return_value = mock_dataframe

    with pytest.raises(ValueError, match="Ожидаемая колонка 'Дата операции' отсутствует"):
        load_transactions_file("fake_path.xlsx")
