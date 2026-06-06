from ib_insync import IB
import logging

def get_ib_connection(host, port, client_id, timeout=5):
    """Creates and validates a connection to the IB API."""
    ib = IB()
    ib.connect(host, port, clientId=client_id, timeout=timeout)

    if not ib.isConnected():
        raise RuntimeError("IB connection failed")

    logging.info("Connected to IB")
    return ib

    