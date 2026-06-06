import plotly.graph_objects as go


def plot_backtest(df, trades=None, title="Strategy Backtest"):
    """
    Visualises:
    - price
    - raw buy/sell signals
    - executed entry/exit trades
    - equity curve
    """

    fig = go.Figure()

    # -----------------------------------
    # PRICE
    # -----------------------------------
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["close"],
        mode="lines",
        name="Close Price"
    ))

    # -----------------------------------
    # RAW BUY SIGNALS
    # -----------------------------------
    if "buy_signal" in df.columns:
        buy_points = df[df["buy_signal"] == 1]

        fig.add_trace(go.Scatter(
            x=buy_points["date"],
            y=buy_points["close"],
            mode="markers",
            name="Buy Signal",
            marker=dict(
                color="rgba(0,255,0,0.35)",
                size=7,
                symbol="circle"
            )
        ))

    # -----------------------------------
    # RAW SELL SIGNALS
    # -----------------------------------
    if "sell_signal" in df.columns:
        sell_points = df[df["sell_signal"] == 1]

        fig.add_trace(go.Scatter(
            x=sell_points["date"],
            y=sell_points["close"],
            mode="markers",
            name="Sell Signal",
            marker=dict(
                color="rgba(255,0,0,0.35)",
                size=7,
                symbol="circle"
            )
        ))

    # -----------------------------------
    # EXECUTED TRADES 
    # -----------------------------------
    if trades:
        entry_x = [t["entry_time"] for t in trades]
        entry_y = [t["entry_price"] for t in trades]

        exit_x = [t["exit_time"] for t in trades]
        exit_y = [t["exit_price"] for t in trades]

        fig.add_trace(go.Scatter(
            x=entry_x,
            y=entry_y,
            mode="markers",
            name="Entry (Executed)",
            marker=dict(
                color="lime",
                size=11,
                symbol="triangle-up",
                line=dict(width=1, color="black")
            )
        ))

        fig.add_trace(go.Scatter(
            x=exit_x,
            y=exit_y,
            mode="markers",
            name="Exit (Executed)",
            marker=dict(
                color="red",
                size=11,
                symbol="triangle-down",
                line=dict(width=1, color="black")
            )
        ))

    # -----------------------------------
    # EQUITY CURVE
    # -----------------------------------
    if "equity" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["equity"],
            mode="lines",
            name="Equity Curve",
            yaxis="y2"
        ))

    # -----------------------------------
    # LAYOUT
    # -----------------------------------
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=True,

        yaxis2=dict(
            title="Equity",
            overlaying="y",
            side="right"
        )
    )

    fig.show()