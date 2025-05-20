import functools
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import pandas as pd


def save_report(filename: Optional[str] = None):
    """Декоратор для сохранения отчета в файл"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            output_file: str = filename or f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logging.info(f"Report saved to {output_file}")
            return result

        return wrapper

    return decorator


@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Dict[str, Any]:
    """Рассчитывает общие траты по заданной категории за 90-дневный период"""
    logging.info(f"Calculating spending for category {category}")

    if date:
        try:
            end_date = pd.to_datetime(date)
        except ValueError:
            logging.error("Invalid date format")
            raise ValueError("Date must be in format YYYY-MM-DD")
    else:
        end_date = pd.to_datetime(datetime.now())

    start_date = end_date - timedelta(days=90)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    df = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
    ]

    total_spent = df["Сумма платежа"].sum()

    return {
        "category": category,
        "total_spent": round(total_spent, 2),
        "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    }
