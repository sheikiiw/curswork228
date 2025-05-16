import json
import logging
from typing import Any

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загружает данные о транзакциях из Excel-файла и возвращает DataFrame."""
    logger.info(f"Загрузка данных из файла: {file_path}")
    try:
        transactions_df = pd.read_excel(file_path)
        if transactions_df.empty:
            raise ValueError("Файл пустой или не содержит данных.")
        logger.info(f"Успешная загрузка. Всего записей: {len(transactions_df)}")
        return transactions_df
    except Exception as error:
        logger.error(f"Ошибка при загрузке данных: {error}")
        raise


def search_transactions(query: str, file_path: str) -> str:
    """Выполняет поиск по всем полям файла на соответствие текстовому запросу."""
    logger.info(f"Поисковый запрос: {query}")
    try:
        query_normalized = query.strip().lower()
        transactions_df = load_transactions(file_path)

        matched_transactions = transactions_df[transactions_df.apply(
            lambda row: row.astype(str).str.contains(query_normalized, case=False, na=False).any(), axis=1
        )]

        logger.info(f"Найдено совпадений: {len(matched_transactions)}")

        response: dict[str, Any] = {
            "query": query,
            "results_count": len(matched_transactions),
            "results": matched_transactions.to_dict(orient="records")
        }

        return json.dumps(response, ensure_ascii=False)

    except Exception as error:
        logger.error(f"Ошибка при поиске: {error}")
        return json.dumps({"ошибка": str(error)}, ensure_ascii=False)


def process_investment_banking():
    """Обрабатывает операции инвестиционного банкинга (заглушка)."""
    return None


if __name__ == "__main__":
    search_query = input("Введите запрос для поиска: ").title()
    result = search_transactions(search_query, "../data/operations.xlsx")
    print(result)


def load_transactions_file():
    return None


def investment_banking_service():
    return None