import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


def read_transactions(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path)
        logging.info(f"Successfully read transactions from {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error reading transactions: {e}")
        raise


def get_greeting(dt: datetime) -> str:
    hour = dt.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Получает курсы валют относительно RUB для указанных валют"""
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        logging.error("EXCHANGE_RATE_API_KEY not set in environment variables")
        return []

    rates = []
    for currency in currencies:
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
            response = requests.get(url, params={"api_key": api_key})
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = response.json()
            rates.append({"currency": currency, "rate": data["rates"]["RUB"]})
        except Exception as e:
            logging.error(f"Error fetching currency {currency}: {e}")
    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получает текущие цены акций для указанных символов"""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        logging.error("ALPHA_VANTAGE_API_KEY not set in environment variables")
        return []

    prices = []
    for stock in stocks:
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = response.json()
            prices.append({"stock": stock, "price": float(data["Global Quote"]["05. price"])})
        except Exception as e:
            logging.error(f"Error fetching stock {stock}: {e}")
    return prices
