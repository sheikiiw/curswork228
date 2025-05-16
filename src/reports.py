import json
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Optional

import pandas as pd


def save_report(file_name: Optional[str] = None):
    """
    Декоратор для сохранения результата функции в JSON-файл.
    Если имя файла не указано — формируется автоматически на основе имени функции и текущей даты.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> str:
            result: str = func(*args, **kwargs)

            nonlocal file_name
            if file_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"report_{func.__name__}_{timestamp}.json"

            try:
                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(result)
                print(f"Отчет успешно сохранен в файл: {file_name}")
            except Exception as error:
                print(f"Ошибка при сохранении отчета: {error}")

            return result
        return wrapper

    # Поддержка вызова декоратора с параметром или без
    if callable(file_name):
        return decorator(file_name)
    return decorator


@save_report
def get_category_expenses(dataframe: pd.DataFrame, category: str, start_date: str) -> str:
    """
    Функция для формирования отчета о расходах по указанной категории за трехмесячный период.
    Возвращает результат в формате JSON.
    """
    try:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = start_date_dt + timedelta(days=90)
        dataframe["date"] = pd.to_datetime(dataframe["date"])

        filtered_dataframe = dataframe[
            (dataframe["category"] == category) &
            (dataframe["date"] >= start_date_dt) &
            (dataframe["date"] <= end_date)
        ]

        if filtered_dataframe.empty:
            return json.dumps({"ошибка": "Нет данных для выбранной категории и периода."}, ensure_ascii=False, indent=4)

        category_expenses = filtered_dataframe.groupby("category")["amount"].sum().reset_index()
        result = category_expenses.to_dict(orient="records")

        return json.dumps(result, ensure_ascii=False, indent=4)

    except Exception as error:
        return json.dumps({"ошибка": str(error)}, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    sample_data = {
        "date": ["2025-01-15", "2025-02-20", "2025-03-10", "2025-03-25", "2025-04-05"],
        "category": ["Food", "Food", "Transport", "Food", "Food"],
        "amount": [100, 200, 50, 150, 100],
    }

    transactions_df = pd.DataFrame(sample_data)

    start_date = "2025-01-01"
    category = "Food"
    result = get_category_expenses(transactions_df, category, start_date)

    print(result)


def category_spending_report():
    return None
