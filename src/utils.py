
import logging
import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

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

def get_currency_rates(currencies: List[str], api_key: str) -> List[Dict[str, Any]]:
    rates = []
    for currency in currencies:
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
            response = json.get(url, params={"api_key": api_key})
            data = response.json()
            rates.append({"currency": currency, "rate": data["rates"]["RUB"]})
        except Exception as e:
            logging.error(f"Error fetching currency {currency}: {e}")
    return rates

def get_stock_prices(stocks: List[str], api_key: str) -> List[Dict[str, Any]]:
    prices = []
    for stock in stocks:
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
            response = json.get(url)
            data = response.json()
            prices.append({"stock": stock, "price": float(data["Global Quote"]["05. price"])})
        except Exception as e:
            logging.error(f"Error fetching stock {stock}: {e}")
    return prices


def load_transactions():
    return None
