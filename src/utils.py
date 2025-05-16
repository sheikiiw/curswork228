import logging
from datetime import datetime

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_datetime_string(date_string: str) -> datetime:
    """Преобразует строку даты и времени в объект datetime."""
    try:
        parsed_datetime = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        logger.info(f"Дата успешно распознана: {parsed_datetime}")
        return parsed_datetime
    except ValueError as error:
        logger.error(f"Ошибка при разборе даты: {error}")
        raise


def fetch_api_data(request_date: datetime) -> list[dict]:
    """Имитация получения данных с API на заданную дату."""
    try:
        logger.info(f"Получение данных с API на дату: {request_date.date()}")
        mock_data = [
            {"value": 100, "date": str(request_date.date())},
            {"value": 150, "date": str(request_date.date())},
            {"value": 200, "date": str(request_date.date())},
        ]
        return mock_data
    except Exception as error:
        logger.error(f"Ошибка API-запроса: {error}")
        raise


def process_data(records: list[dict]) -> dict:
    """Анализирует данные, рассчитывая среднее значение и количество записей."""
    try:
        dataframe = pd.DataFrame(records)
        logger.info("Данные успешно преобразованы в DataFrame")

        if 'value' in dataframe.columns:
            average_value = dataframe['value'].mean()
        else:
            average_value = None
            logger.warning("Колонка 'value' отсутствует в данных")

        return {
            "average_value": average_value,
            "records_count": len(dataframe)
        }
    except Exception as error:
        logger.error(f"Ошибка анализа данных: {error}")
        raise


def load_transactions_file(file_path: str) -> pd.DataFrame:
    """Загружает данные о транзакциях из Excel-файла и возвращает DataFrame."""
    try:
        logger.info(f"Чтение Excel-файла: {file_path}")
        transactions_df = pd.read_excel(file_path)

        if 'Дата операции' not in transactions_df.columns:
            logger.error("Колонка 'Дата операции' не найдена в Excel-файле")
            raise ValueError("Ожидаемая колонка 'Дата операции' отсутствует")

        return transactions_df
    except Exception as error:
        logger.error(f"Ошибка загрузки данных: {error}")
        raise


def process_transactions():
    """Обрабатывает транзакции (заглушка)."""
    return None


if __name__ == "__main__":
    transactions_dataframe = load_transactions_file("../data/operations.xlsx")
    print(transactions_dataframe)


def load_transactions():
    return None