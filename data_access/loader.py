import duckdb
import pandas as pd
from data_access.paths import get_db_path
from config import TIMEFRAMES


def load_data(
    contract,
    timeframe="1day",
    order_by_date=True
):
    """
    Load historical market data for a given IB contract.
    """
    
    if timeframe not in TIMEFRAMES:
        raise ValueError(f"Invalid timeframe: {timeframe}")

    db_path = get_db_path(contract)
    table = f"price_data_{timeframe}"

    conn = duckdb.connect(str(db_path))

    df = conn.execute(f"""
        SELECT *
        FROM {table}
    """).df()

    conn.close()

    # ---------------------------------------
    # CLEAN DATA
    # ---------------------------------------

    df["date"] = pd.to_datetime(df["date"], utc=True)

    if order_by_date:
        df = df.sort_values("date").reset_index(drop=True)

    return df