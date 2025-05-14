import json
from datetime import datetime
import pandas as pd
from typing import Dict, Any
from src.utils import read_transactions, get_greeting, get_currency_rates, get_stock_prices
import logging


def home_page(date_time: str) -> Dict[str, Any]:
    logging.info(f"Generating Home page response for {date_time}")

    try:
        dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logging.error("Invalid date format")
        raise ValueError("Date must be in format YYYY-MM-DD HH:MM:SS")
    with open("user_settings.json") as f:
        settings = json.load(f)


    df = read_transactions("data/operations.xlsx")

    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    start_date = dt.replace(day=1, hour=0, minute=0, second=0)
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= dt)]


    cards = []
    for card in df["Номер карты"].unique():
        if pd.notna(card):
            card_df = df[df["Номер карты"] == card]
            total_spent = card_df["Сумма платежа"].sum()
            cashback = total_spent / 100  # 1 рубль за 100 рублей
            cards.append({
                "last_digits": card[-4:],
                "total_spent": round(total_spent, 2),
                "cashback": round(cashback, 2)
            })

    top_transactions = df.sort_values("Сумма платежа", ascending=False).head(5)[
        ["Дата операции", "Сумма платежа", "Категория", "Описание"]
    ].to_dict(orient="records")

    currency_rates = get_currency_rates(settings["user_currencies"], "your_api_key")
    stock_prices = get_stock_prices(settings["user_stocks"], "your_api_key")

    return {
        "greeting": get_greeting(dt),
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
