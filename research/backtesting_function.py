from strategies.signals import add_buy_sell_signals


def run_backtest(df, initial_cash=10000):
    position = 0    # internal state tracker for position held in the market
    cash = initial_cash
    entry_price = 0
    exit_price = 0

    equity_curve = []
    trades = []

    entry_time = None
    exit_time = None

    add_buy_sell_signals(df,price=df["close"], fast_window=20, slow_window=50)

    for i in range(len(df)):
        price = df["close"].iloc[i]
        date = df["date"].iloc[i]

        buy = df["buy_signal"].iloc[i]
        sell = df["sell_signal"].iloc[i]

        # buy
        if buy and position == 0:
            position = 1
            entry_price = price
            entry_time = date 

        # sell
        elif sell and position == 1:
            position = 0
            return_pct = (price - entry_price) / entry_price
            cash = cash * (1 + return_pct)  # profit loss calculation
            exit_price = price
            exit_time = date 
            trades.append({
                "entry_time": entry_time,
                "entry_price": entry_price,
                "exit_time": exit_time,
                "exit_price": exit_price,
                "return_pct": return_pct
            })

        # profit loss calculation for total current equity 
        if position == 1:
            equity = cash * (price / entry_price)
        else:
            equity = cash



        equity_curve.append(equity)
    df = df.copy()
    df["equity"] = equity_curve
    return df, trades

        
        








