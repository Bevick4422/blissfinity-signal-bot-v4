import asyncio
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


async def main():

    print("V4 BOT STARTED")

    try:
        await send_message(
            "✅ Blissfinity V4 Online"
        )
    except:
        pass

    while True:

        try:

            trades = load_trades()

            history = load_signals()

            today = datetime.now(UTC).strftime("%Y-%m-%d")
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

                trend_df, entry_df = get_market_data(
                    symbol,
                    TREND_TIMEFRAME,
                    ENTRY_TIMEFRAME
                )

                if trend_df is None:
                    continue

                if entry_df is None:
                    continue

                active_trade = any(

                    trade["pair"] == symbol

                    for trade in trades

                )

                if active_trade:

                    print(
                        f"{symbol} active"
                    )

                    continue

                direction = None

                if (
                    bullish_structure(trend_df)
                    and
                    bullish_setup(entry_df)
                ):

                    direction = "LONG"

                elif (
                    bearish_structure(trend_df)
                    and
                    bearish_setup(entry_df)
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
                        entry * 0.95,
                        4
                    )

                    tp1 = round(
                        entry * 1.05,
                        4
                    )

                    tp2 = round(
                        entry * 1.10,
                        4
                    )

                else:

                    sl = round(
                        entry * 1.05,
                        4
                    )

                    tp1 = round(
                        entry * 0.95,
                        4
                    )

                    tp2 = round(
                        entry * 0.90,
                        4
                    )

                message = f"""
🚀 NEW SIGNAL

Pair: {symbol}
Direction: {direction}

Entry: {entry}
TP1: {tp1}
TP2: {tp2}
SL: {sl}
"""

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

                save_trades(
                    trades
                )

                signals_today += 1

                history["count"] = signals_today

                save_signals(
                    history
                )

                print(
                    f"{symbol} stored"
                )

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