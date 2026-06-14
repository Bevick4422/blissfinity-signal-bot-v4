import json
import os

SIGNAL_FILE = "signals.json"


def load_signals():

    if not os.path.exists(SIGNAL_FILE):
        return {}

    try:

        with open(SIGNAL_FILE, "r") as f:
            return json.load(f)

    except:
        return {}


def save_signals(data):

    with open(SIGNAL_FILE, "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )