import json
import unittest

import pandas as pd

from src.reports import get_category_expenses


class TestCategoryExpenses(unittest.TestCase):

    def setUp(self):
        """Настройка тестовых данных."""
        test_data = {
            "date": ["2025-01-15", "2025-02-20", "2025-03-10", "2025-03-25", "2025-04-05"],
            "category": ["Food", "Food", "Transport", "Food", "Food"],
            "amount": [100, 200, 50, 150, 100],
        }
        self.transactions_df = pd.DataFrame(test_data)

    def test_category_expenses(self):
        """Тест с корректными данными для категории."""
        start_date = "2025-01-01"
        category = "Food"
        result = get_category_expenses(self.transactions_df, category, start_date)

        expected_result = [{"category": "Food", "amount": 450}]

        self.assertEqual(json.loads(result), expected_result)

    def test_no_data_for_category(self):
        """Тест, когда данные для категории ограничены."""
        start_date = "2025-01-01"
        category = "Transport"
        result = get_category_expenses(self.transactions_df, category, start_date)

        expected_result = [{"category": "Transport", "amount": 50}]

        self.assertEqual(json.loads(result), expected_result)

    def test_no_data_for_date_range(self):
        """Тест, когда нет данных за указанный период."""
        start_date = "2024-01-01"
        category = "Food"
        result = get_category_expenses(self.transactions_df, category, start_date)
        expected_result = {"ошибка": "Нет данных для выбранной категории и периода."}

        self.assertEqual(json.loads(result), expected_result)

    def test_empty_dataframe(self):
        """Тест с пустым DataFrame."""
        empty_dataframe = pd.DataFrame(columns=["date", "category", "amount"])
        start_date = "2025-01-01"
        category = "Food"
        result = get_category_expenses(empty_dataframe, category, start_date)

        expected_result = {"ошибка": "Нет данных для выбранной категории и периода."}

        self.assertEqual(json.loads(result), expected_result)

    def test_invalid_date_format(self):
        """Тест с некорректным форматом даты."""
        start_date = "2025/01/01"
        category = "Food"
        result = get_category_expenses(self.transactions_df, category, start_date)
        self.assertIn("time data", json.loads(result)["ошибка"])


if __name__ == "__main__":
    unittest.main()
