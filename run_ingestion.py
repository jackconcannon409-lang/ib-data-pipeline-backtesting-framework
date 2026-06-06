from ib_insync import Stock, Forex
from data_ingestion.contract_ingestion import ingest_contract
import time


CONTRACTS = [
    Stock("AAPL", "SMART", "USD")
]
TIMEFRAME="1day"

def main():
    for contract in CONTRACTS:
        print(f"Ingesting {contract.symbol}...")

        try:
            ingest_contract(contract, timeframe=TIMEFRAME)
            time.sleep(2)

        except Exception as e:
            print(f"Failed {contract.symbol}: {e}")


if __name__ == "__main__":
    main()