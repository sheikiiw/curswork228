from src.views import display_home_page
from src.services import investment_banking_service
from src.reports import category_spending_report
import pandas as pd
from src.utils import load_transactions


def main():
    transactions_df = load_transactions("data/operations.xlsx")

    print("Home Page:", display_home_page("2025-05-14 14:00:00"))

    transaction_records = transactions_df.to_dict(orient="records")
    print("Investment Banking:", investment_banking_service("2025-05", transaction_records, 50))

    print("Category Spending:", category_spending_report(transactions_df, "Супермаркеты"))


if __name__ == "__main__":
    main()