# ib-data-pipeline
A Python-based trading research system for ingesting Interactive Brokers historical data, storing it in DuckDB, generating indicators, and running event-driven strategy backtests with visualisation tools.

## Features

- Interactive Brokers historical data ingestion
- Local storage using DuckDB
- Modular indicator system (SMA, RSI, Bollinger Bands, etc.)
- Strategy signal generation framework
- Event-driven backtesting engine
- Trade tracking (entries/exits, PnL)
- Interactive Plotly visualisation of:
  - Price action
  - Buy/sell signals
  - Executed trades
  - Equity curve


## Architecture

The system is structured into modular components:

- data_access → Loads historical market data from DuckDB
- data_ingestion → Handles IB contract ingestion
- features → Technical indicators (SMA, RSI, Bollinger Bands)
- strategies → Signal generation logic
- research → Backtesting engine
- visualisation → Plotting and analysis tools


## Workflow

1. Load historical market data from DuckDB
2. Generate technical indicators
3. Create buy/sell signals from strategy rules
4. Run event-driven backtest
5. Track positions, equity, and trades
6. Visualise results interactively

## Example Usage

```python
from ib_insync import Stock
from data_access.loader import load_data
from research.backtesting_function import run_backtest
from visualisation.backtest_plot import plot_backtest

contract = Stock("AAPL", "SMART", "USD")

df = load_data(contract, timeframe="1day")
df, trades = run_backtest(df)

plot_backtest(df, trades)


---

## 7. Project structure (simple, not verbose)

```md
## Project Structure

data_access/
data_ingestion/
features/
strategies/
research/
visualisation/


## Future Improvements

- Portfolio-level backtesting
- Transaction cost + slippage modelling
- Walk-forward optimisation
- Strategy parameter tuning engine
- Live trading integration with IB API

