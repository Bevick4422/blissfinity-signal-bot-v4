import json
import os

COMPLETED_FILE = "completed_trades.json"


def load_completed():

    if not os.path.exists(COMPLETED_FILE):
        return []

    with open(
        COMPLETED_FILE,
        "r"
    ) as f:

        return json.load(f)


def save_completed(trades):

    with open(
        COMPLETED_FILE,
        "w"
    ) as f:

        json.dump(
            trades,
            f,
            indent=4
        )