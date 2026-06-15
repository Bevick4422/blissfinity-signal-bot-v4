from datetime import datetime

from trade_storage import (
    load_trades,
    save_trades,
    load_completed_trades,
    save_completed_trades
)

from price_fetcher import (
    get_price
)

from telegram_sender import (
    send_message
)


async def check_trades():

    print("TRACKER RUNNING")

    trades = load_trades()

    completed = load_completed_trades()

    active = []

    for trade in trades:

        price = get_price(
            trade["pair"]
        )

        if price is None:

            active.append(trade)

            continue

        closed = False

        entry = trade["entry"]

        risk = abs(
            entry - trade["sl"]
        )

        # ==========================
        # LONG
        # ==========================

        if trade["direction"] == "LONG":

            if (
                not trade["tp1_hit"]
                and price >= trade["tp1"]
            ):

                await send_message(
                    f"🎯 TP1 HIT\n\n{trade['pair']}"
                )

                trade["tp1_hit"] = True

            if (
                not trade["tp2_hit"]
                and price >= trade["tp2"]
            ):

                rr = round(
                    (
                        trade["tp2"] - entry
                    ) / risk,
                    2
                )

                await send_message(
                    f"🚀 TP2 HIT\n\n{trade['pair']}\nRR: {rr}R"
                )

                completed.append({

                    **trade,

                    "result": "TP2",

                    "rr": rr,

                    "closed_at": str(
                        datetime.utcnow()
                    )

                })

                closed = True

            elif (
                not trade["sl_hit"]
                and price <= trade["sl"]
            ):

                await send_message(
                    f"🛑 STOPLOSS HIT\n\n{trade['pair']}"
                )

                completed.append({

                    **trade,

                    "result": "SL",

                    "rr": -1,

                    "closed_at": str(
                        datetime.utcnow()
                    )

                })

                closed = True

        # ==========================
        # SHORT
        # ==========================

        elif trade["direction"] == "SHORT":

            if (
                not trade["tp1_hit"]
                and price <= trade["tp1"]
            ):

                await send_message(
                    f"🎯 TP1 HIT\n\n{trade['pair']}"
                )

                trade["tp1_hit"] = True

            if (
                not trade["tp2_hit"]
                and price <= trade["tp2"]
            ):

                rr = round(
                    (
                        entry - trade["tp2"]
                    ) / risk,
                    2
                )

                await send_message(
                    f"🚀 TP2 HIT\n\n{trade['pair']}\nRR: {rr}R"
                )

                completed.append({

                    **trade,

                    "result": "TP2",

                    "rr": rr,

                    "closed_at": str(
                        datetime.utcnow()
                    )

                })

                closed = True

            elif (
                not trade["sl_hit"]
                and price >= trade["sl"]
            ):

                await send_message(
                    f"🛑 STOPLOSS HIT\n\n{trade['pair']}"
                )

                completed.append({

                    **trade,

                    "result": "SL",

                    "rr": -1,

                    "closed_at": str(
                        datetime.utcnow()
                    )

                })

                closed = True

        if not closed:

            active.append(trade)

    save_trades(active)

    save_completed_trades(completed)