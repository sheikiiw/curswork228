import logging
from datetime import datetime

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_datetime_string(date_string: str) -> datetime:
    """Преобразует строку с датой и временем в объект datetime."""
    try:
        parsed_datetime = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        logger.info(f"Успешный парсинг: {parsed_datetime}")
        return parsed_datetime
    except ValueError as error:
        logger.error(f"Ошибка парсинга даты: {error}")
        raise


def fetch_api_data(request_date: datetime) -> list[dict]:
    """Получает данные с внешнего API по дате (заглушка)."""
    try:
        logger.info(f"Запрос данных с API для даты: {request_date.date()}")
        return [
            {"value": 100, "date": str(request_date.date())},
            {"value": 150, "date": str(request_date.date())},
            {"value": 200, "date": str(request_date.date())}
        ]
    except Exception as error:
        logger.error(f"Ошибка при запросе к API: {error}")
        raise


def process_data(records: list[dict]) -> dict:
    """Обрабатывает данные с использованием pandas и возвращает статистику."""
    try:
        dataframe = pd.DataFrame(records)
        logger.info("Данные успешно преобразованы в DataFrame")

        if 'value' not in dataframe.columns:
            logger.warning("Колонка 'value' не найдена")
            average_value = None
        else:
            average_value = dataframe['value'].mean()

        return {
            "average_value": average_value,
            "records_count": len(dataframe)
        }
    except Exception as error:
        logger.error(f"Ошибка при анализе данных: {error}")
        raise


def load_transactions_file(file_path: str) -> pd.DataFrame:
    """Загружает данные о транзакциях из Excel-файла."""
    try:
        logger.info(f"Загрузка данных из файла: {file_path}")
        transactions_df = pd.read_excel(file_path)

        if 'Дата операции' not in transactions_df.columns:
            error_message = "Не найдена колонка 'Дата операции' в файле."
            logger.error(error_message)
            raise ValueError(error_message)

        return transactions_df
    except Exception as error:
        logger.error(f"Ошибка при загрузке данных из файла: {error}")
        raise


def render_home_page():
    """Отображает домашнюю страницу (заглушка)."""
    return None


def show_home_page():
    """Показывает домашнюю страницу (заглушка)."""
    return None


if __name__ == "__main__":
    try:
        transactions_dataframe = load_transactions_file("../data/operations.xlsx")
        print(transactions_dataframe)
    except Exception as error:
        logger.error(f"Не удалось загрузить данные: {error}")


def display_home_page():
    return None
