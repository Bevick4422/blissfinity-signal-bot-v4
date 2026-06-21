import json
import os

COMPLETED_FILE = "completed_trades.json"


def get_stats():

    if not os.path.exists(COMPLETED_FILE):
        return None

    try:

        with open(COMPLETED_FILE, "r") as f:
            trades = json.load(f)

        if not isinstance(trades, list):
            return None

        if len(trades) == 0:
            return None

        total = len(trades)

        wins = len(
            [t for t in trades if t["rr"] > 0]
        )

        losses = len(
            [t for t in trades if t["rr"] < 0]
        )

        total_rr = round(
            sum(
                float(t["rr"])
                for t in trades
            ),
            2
        )

        winrate = round(
            wins / total * 100,
            2
        )

        avg_rr = round(
            total_rr / total,
            2
        )

        return {
            "total": total,
            "wins": wins,
            "losses": losses,
            "winrate": winrate,
            "total_rr": total_rr,
            "avg_rr": avg_rr
        }

    except:

        return None