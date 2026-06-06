from config import DATA_ROOT
from ib_insync import Stock, Forex, Option, Bond, CFD, Index, Future


# -------------------------------------------
# CONTRACT CLASSIFICATION
# -------------------------------------------

TYPE_MAP = {
    Stock: ("equities", "stocks"),
    Forex: ("forex", "spot"),
    Future: ("futures", "contracts"),
    Option: ("options", "contracts"),
    Bond: ("fixed_income", "bonds"),
    CFD: ("cfds", "spot"),
    Index: ("indices", "spot"),
}


def classify_contract(contract):
    return TYPE_MAP.get(type(contract), ("other", "misc"))


# -------------------------------------------
# PATH HELPERS
# -------------------------------------------

def get_contract_filename(contract):
    symbol = getattr(contract, "symbol", "unknown")
    exchange = getattr(contract, "exchange", "na")
    currency = getattr(contract, "currency", "na")

    return f"{symbol}_{exchange}_{currency}.duckdb"


def get_db_path(contract):
    market, subtype = classify_contract(contract)

    path = (
        DATA_ROOT /
        market /
        subtype /
        get_contract_filename(contract)
    )

    path.parent.mkdir(parents=True, exist_ok=True)

    return path