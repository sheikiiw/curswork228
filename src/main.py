from src.reports import spending_by_category
from src.services import investment_bank
from src.utils import read_transactions
from src.views import home_page


def main():
    df = read_transactions("data/operations.xlsx")
    print("Home Page:", home_page("2025-05-14 14:00:00"))
    transactions = df.to_dict(orient="records")
    print("Investment Bank:", investment_bank("2025-05", transactions, 50))
    print("Spending by Category:", spending_by_category(df, "Супермаркеты"))


if __name__ == "__main__":
    main()
