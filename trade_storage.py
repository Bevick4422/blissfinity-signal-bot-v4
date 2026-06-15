import json
import os

TRADE_FILE = "active_trades.json"
COMPLETED_FILE = "completed_trades.json"


def load_trades():

    if not os.path.exists(TRADE_FILE):
        return []

    with open(
        TRADE_FILE,
        "r"
    ) as f:

        return json.load(f)


def save_trades(trades):

    with open(
        TRADE_FILE,
        "w"
    ) as f:

        json.dump(
            trades,
            f,
            indent=4
        )


def load_completed_trades():

    if not os.path.exists(COMPLETED_FILE):
        return []

    with open(
        COMPLETED_FILE,
        "r"
    ) as f:

        return json.load(f)


def save_completed_trades(trades):

    with open(
        COMPLETED_FILE,
        "w"
    ) as f:

        json.dump(
            trades,
            f,
            indent=4
        )