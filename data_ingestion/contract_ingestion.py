import pandas as pd
import duckdb
from ib_insync import util
import time
import logging

from data_access.paths import get_db_path
from data_access.ib_connection import get_ib_connection
from config import (
    IB_HOST,
    IB_PORT, 
    CLIENT_ID, 
    FORMAT_DATE, 
    USE_RTH, 
    WHAT_TO_SHOW,
    TIMEFRAMES
)

# -------------------------------------------
# LOGGING
# -------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -------------------------------------------
# CORE INGESTION FUNCTION
# -------------------------------------------

def ingest_contract(
    contract,
    timeframe="1day",
    until_date=None, #YYYY-MM-DD
    disable_limits=False
):
    
    """
    Ingest historical market data for a single IB contract into DuckDB.
    """

    if until_date is not None:
        until_date = pd.to_datetime(until_date, utc=True)
    # ---------------------------------------
    # IB API CONNECT
    # ---------------------------------------

    ib = get_ib_connection(IB_HOST, IB_PORT, CLIENT_ID)
    
    contract = ib.qualifyContracts(contract)[0]

    # ---------------------------------------
    # TIMEFRAME CONFIG
    # ---------------------------------------

    if timeframe not in TIMEFRAMES:
        raise ValueError(f"Invalid timeframe: {timeframe}")


    cfg = TIMEFRAMES[timeframe]
    bar_size = cfg["bar_size"]
    duration = cfg["duration"]
    
    
    # ---------------------------------------
    # DATABASE SETUP
    # ---------------------------------------

    db_path = get_db_path(contract)
    conn = duckdb.connect(str(db_path))

    table = f"price_data_{timeframe}"

    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS {table} (
        conId INTEGER,
        date TIMESTAMP,
        open DOUBLE,
        high DOUBLE,
        low DOUBLE,
        close DOUBLE,
        volume DOUBLE,
        PRIMARY KEY(conId, date)
    )
    """)

    # ---------------------------------------
    # DETERMINE CUTOFF DATE FOR INCREMENTAL FETCH
    # ---------------------------------------

    # for early stopping optimisation in fetch loop
    raw_max_date = conn.execute(
        f"SELECT MAX(date) FROM {table}"
    ).fetchone()[0]

    db_max_date = pd.to_datetime(raw_max_date, utc=True) if raw_max_date else None

    # ---------------------------------------
    # FETCH LOOP
    # ---------------------------------------

    end_time = None   # starting time for earliest bar data, NONE is the present
    request_count = 0

    # IB API requests data from end_time back
    # While loop circumvents bar restrictions IB applies, fetching chunks at a time
    while True:
        try:
            bars = ib.reqHistoricalData(
                contract,
                endDateTime=end_time or "",
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow=WHAT_TO_SHOW,
                useRTH=USE_RTH,
                formatDate=FORMAT_DATE
            )

        except Exception as e:
            logging.error(f"IB request failed: {e}")
            break

        if not bars:
            logging.info("No more bars returned - stopping.")
            break

        df = util.df(bars)

        df["conId"] = contract.conId
        df["date"] = pd.to_datetime(df["date"], utc=True)
        df["conId"] = df["conId"].astype("int64")

        df = df[["conId", "date", "open", "high", "low", "close", "volume"]]

        logging.info(
            f"{contract.symbol} | Chunk {request_count} | "
            f"{df['date'].min()} → {df['date'].max()} | "
            f"{len(df)} rows"
        )

        request_count += 1

        # ---------------------------------------
        # STOPPING CONDITIONS
        # ---------------------------------------

        # stop once there is a full overlap in bar data requested and existing data stored in db
        if db_max_date is not None and df["date"].max() <= db_max_date:
            logging.info("Reached existing database coverage.")
            break

        # stop if we reached user-defined cutoff
        if until_date is not None and df["date"].min() <= until_date:
            logging.info(f"Reached cutoff date: {until_date}")
            break

        # stop if we reach data request limits, used to stop long data requests for safety
        if not disable_limits:
            if cfg["max_requests"] is not None and request_count >= cfg["max_requests"]:
                logging.info("Max request limit reached — stopping.")
                break

        # getting rid of duplicates within bathes
        df = df.sort_values("date")
        df = df.drop_duplicates(subset=["conId", "date"], keep="last")

        # Register DataFrame so it can be used in SQL INSERT statement
        conn.register("batch", df)

        # merging new bar data with existing data and skipping duplicates
        conn.execute(f"""
            INSERT INTO {table}
            SELECT * FROM batch
            ON CONFLICT(conId, date) DO NOTHING
        """)

        end_time = df["date"].min().strftime("%Y%m%d-%H:%M:%S")
        time.sleep(1)

    # ---------------------------------------
    # CLEANUP
    # ---------------------------------------

    logging.info(f"Finished ingestion for {contract.symbol}")

    ib.disconnect()
    conn.close()