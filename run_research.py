from ib_insync import Stock
from data_access.loader import load_data
from research.backtesting_function import run_backtest

def main():
    
    contract = Stock("AAPL", "SMART", "USD")
    df = load_data(contract, timeframe="1day")
    result = run_backtest(df)

    return result


if __name__ == "__main__":
    main()