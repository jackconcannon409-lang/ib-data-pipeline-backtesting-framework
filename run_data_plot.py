from ib_insync import Stock
from data_access.loader import load_data
from research.backtesting_function import run_backtest
from visualisation.backtest_plot import plot_backtest


def main():
    contract = Stock("AAPL", "SMART", "USD")
    df = load_data(contract, timeframe="1day")

    df, trades = run_backtest(df)

    plot_backtest(df, trades, title="AAPL Backtest")


if __name__ == "__main__":
    main()