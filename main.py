from src.views import main_view
from src.services import return_search
from src.reports import day_spending
import pandas as pd


def main():
    path = "data/operations.xlsx"
    df = pd.read_excel(path)
    main_view(path, "2019.5.17 0:0:0")
    return_search(df)
    day_spending(df)

main()