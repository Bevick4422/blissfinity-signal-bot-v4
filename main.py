import asyncio
import json
import os
from datetime import datetime, UTC

from config import (
    SYMBOLS,
    TREND_TIMEFRAME,
    ENTRY_TIMEFRAME,
    MAX_SIGNALS
)

from scanner import get_market_data

from signal_engine import (
    bullish_structure,
    bearish_structure,
    bullish_setup,
    bearish_setup
)

from signal_storage import (
    load_signals,
    save_signals
)

from trade_storage import (
    load_trades,
    save_trades
)

from trade_tracker import check_trades

from telegram_sender import send_message

from weekly_report import build_weekly_report

WEEKLY_FILE = "weekly_report_state.json"


def load_weekly_state():

    if not os.path.exists(WEEKLY_FILE):

        return {
            "week": ""
        }

    try:

        with open(WEEKLY_FILE, "r") as f:

            return json.load(f)

    except:

        return {
            "week": ""
        }


def save_weekly_state(data):

    with open(WEEKLY_FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )


async def send_weekly_report():

    now = datetime.now(UTC)

    weekly_state = load_weekly_state()

    current_week = now.strftime("%Y-W%U")

    if (
        now.weekday() == 6
        and now.hour >= 20
        and weekly_state.get("week") != current_week
    ):

        report = build_weekly_report()

        await send_message(report)

        weekly_state["week"] = current_week

        save_weekly_state(
            weekly_state
        )

        print("Weekly report sent")


async def scan_markets():

    today = datetime.now(
        UTC
    ).strftime("%Y-%m-%d")

    trades = load_trades()

    history = load_signals()

    if history.get("date") != today:

        history = {
            "date": today,
            "count": 0
        }

    signals_today = history.get(
        "count",
        0
    )

    for symbol in SYMBOLS:

        if signals_today >= MAX_SIGNALS:

            print(
                f"Daily limit reached ({MAX_SIGNALS})"
            )

            break

        active_trade = any(

            trade["pair"] == symbol

            for trade in trades

        )

        if active_trade:

            continue

        trend_df, entry_df = (
            get_market_data(
                symbol,
                TREND_TIMEFRAME,
                ENTRY_TIMEFRAME
            )
        )

        if trend_df is None:

            continue

        if entry_df is None:

            continue

        direction = None

        if (
            bullish_structure(
                trend_df
            )
            and
            bullish_setup(
                entry_df
            )
        ):

            direction = "LONG"

        elif (
            bearish_structure(
                trend_df
            )
            and
            bearish_setup(
                entry_df
            )
        ):

            direction = "SHORT"

        if direction is None:

            continue

        entry = round(
            float(
                entry_df["close"].iloc[-1]
            ),
            4
        )

        if direction == "LONG":

            sl = round(
                entry * 0.985,
                4
            )

            tp1 = round(
                entry * 1.03,
                4
            )

            tp2 = round(
                entry * 1.06,
                4
            )

        else:

            sl = round(
                entry * 1.015,
                4
            )

            tp1 = round(
                entry * 0.97,
                4
            )

            tp2 = round(
                entry * 0.94,
                4
            )

        message = (
            f"🚀 NEW SIGNAL\n\n"
            f"Pair: {symbol}\n"
            f"Direction: {direction}\n\n"
            f"Entry: {entry}\n"
            f"TP1: {tp1}\n"
            f"TP2: {tp2}\n"
            f"SL: {sl}"
        )

        await send_message(
            message
        )

        trades.append({

            "pair": symbol,
            "direction": direction,
            "entry": entry,
            "tp1": tp1,
            "tp2": tp2,
            "sl": sl,
            "tp1_hit": False,
            "tp2_hit": False,
            "sl_hit": False

        })

        save_trades(trades)

        signals_today += 1

        history["count"] = (
            signals_today
        )

        save_signals(history)

        print(
            f"{symbol} stored"
        )


async def main():

    print(
        "BLISSFINITY BOT STARTED"
    )

    try:

        await send_message(
            "✅ Blissfinity Bot Online"
        )

    except Exception as e:

        print(
            f"Startup Telegram Error: {e}"
        )

    while True:

        try:

            await send_weekly_report()

            await scan_markets()

            await check_trades()

            print(
                "Bot Running..."
            )

            await asyncio.sleep(
                300
            )

        except Exception as e:

            print(
                f"Loop Error: {e}"
            )

            await asyncio.sleep(
                30
            )


if __name__ == "__main__":

    asyncio.run(main())