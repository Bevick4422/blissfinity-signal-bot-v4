import json
import os

TRADE_FILE = "active_trades.json"


def load_trades():

    if not os.path.exists(
        TRADE_FILE
    ):
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