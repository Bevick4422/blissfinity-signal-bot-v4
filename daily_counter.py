import json
import os
from datetime import datetime

FILE = "daily_counter.json"


def get_today():

    return datetime.utcnow().strftime("%Y-%m-%d")


def load_counter():

    if not os.path.exists(FILE):

        return {
            "date": get_today(),
            "count": 0
        }

    with open(FILE, "r") as f:

        data = json.load(f)

    if data["date"] != get_today():

        data = {
            "date": get_today(),
            "count": 0
        }

    return data


def can_send_signal():

    data = load_counter()

    return data["count"] < 4


def increment_counter():

    data = load_counter()

    data["count"] += 1

    with open(FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )