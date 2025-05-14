import json
from datetime import datetime
from typing import List, Dict, Any
import logging


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> Dict[str, float]:
    logging.info(f"Calculating Investment Bank for {month} with limit {limit}")

    try:
        month_dt = datetime.strptime(month, "%Y-%m")
    except ValueError:
        logging.error("Invalid month format")
        raise ValueError("Month must be in format YYYY-MM")

    if limit not in [10, 50, 100]:
        logging.error("Invalid limit")
        raise ValueError("Limit must be 10, 50, or 100")

    total_saved = sum(
        (limit - (t["Сумма операции"] % limit)) % limit
        for t in transactions
        if datetime.strptime(t["Дата операции"], "%Y-%m-%d").strftime("%Y-%m") == month
    )

    return {"total_saved": round(total_saved, 2)}