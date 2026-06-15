import json
import os

COMPLETED_FILE = "completed_trades.json"


def get_stats():

    if not os.path.exists(COMPLETED_FILE):
        return "No completed trades yet."

    with open(COMPLETED_FILE, "r") as f:
        trades = json.load(f)

    if len(trades) == 0:
        return "No completed trades yet."

    total = len(trades)

    wins = len(
        [t for t in trades if t["rr"] > 0]
    )

    losses = len(
        [t for t in trades if t["rr"] < 0]
    )

    total_rr = round(
        sum(t["rr"] for t in trades),
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

    return (
        f"📊 BLISSFINITY STATS\n\n"
        f"Trades: {total}\n"
        f"Wins: {wins}\n"
        f"Losses: {losses}\n\n"
        f"Win Rate: {winrate}%\n"
        f"Total RR: {total_rr}R\n"
        f"Average RR: {avg_rr}R"
    )