from datetime import datetime, UTC

from trade_storage import (
    load_trades,
    save_trades
)

from completed_storage import (
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

    active_trades = []

    for trade in trades:

        try:

            price = get_price(
                trade["pair"]
            )

            if price is None:

                active_trades.append(
                    trade
                )

                continue

            entry = float(
                trade["entry"]
            )

            sl = float(
                trade["sl"]
            )

            risk = abs(
                entry - sl
            )

            closed = False

            # ======================
            # LONG TRADES
            # ======================

            if trade["direction"] == "LONG":

                # TP1

                if (
                    not trade["tp1_hit"]
                    and price >= trade["tp1"]
                ):

                    trade["tp1_hit"] = True

                    await send_message(
f"""🎯 TP1 HIT

{trade['pair']}
LONG

Entry: {trade['entry']}
TP1: {trade['tp1']}"""
                    )

                # TP2

                if (
                    not trade["tp2_hit"]
                    and price >= trade["tp2"]
                ):

                    trade["tp2_hit"] = True

                    rr = round(
                        (
                            trade["tp2"]
                            - entry
                        ) / risk,
                        2
                    )

                    await send_message(
f"""🔥🔥🔥 TP2 SMASHED

{trade['pair']}
LONG

Entry: {trade['entry']}
TP2: {trade['tp2']}

RR: {rr}R"""
                    )

                    completed.append({

                        **trade,

                        "result": "TP2",

                        "rr": rr,

                        "closed_at": str(
                            datetime.now(
                                UTC
                            )
                        )

                    })

                    closed = True

                # SL

                elif (
                    not trade["sl_hit"]
                    and price <= trade["sl"]
                ):

                    trade["sl_hit"] = True

                    await send_message(
f"""🛑 STOPLOSS HIT

{trade['pair']}
LONG

Entry: {trade['entry']}
SL: {trade['sl']}"""
                    )

                    completed.append({

                        **trade,

                        "result": "SL",

                        "rr": -1,

                        "closed_at": str(
                            datetime.now(
                                UTC
                            )
                        )

                    })

                    closed = True

            # ======================
            # SHORT TRADES
            # ======================

            elif trade["direction"] == "SHORT":

                # TP1

                if (
                    not trade["tp1_hit"]
                    and price <= trade["tp1"]
                ):

                    trade["tp1_hit"] = True

                    await send_message(
f"""🎯 TP1 HIT

{trade['pair']}
SHORT

Entry: {trade['entry']}
TP1: {trade['tp1']}"""
                    )

                # TP2

                if (
                    not trade["tp2_hit"]
                    and price <= trade["tp2"]
                ):

                    trade["tp2_hit"] = True

                    rr = round(
                        (
                            entry
                            - trade["tp2"]
                        ) / risk,
                        2
                    )

                    await send_message(
f"""🔥🔥🔥 TP2 SMASHED

{trade['pair']}
SHORT

Entry: {trade['entry']}
TP2: {trade['tp2']}

RR: {rr}R"""
                    )

                    completed.append({

                        **trade,

                        "result": "TP2",

                        "rr": rr,

                        "closed_at": str(
                            datetime.now(
                                UTC
                            )
                        )

                    })

                    closed = True

                # SL

                elif (
                    not trade["sl_hit"]
                    and price >= trade["sl"]
                ):

                    trade["sl_hit"] = True

                    await send_message(
f"""🛑 STOPLOSS HIT

{trade['pair']}
SHORT

Entry: {trade['entry']}
SL: {trade['sl']}"""
                    )

                    completed.append({

                        **trade,

                        "result": "SL",

                        "rr": -1,

                        "closed_at": str(
                            datetime.now(
                                UTC
                            )
                        )

                    })

                    closed = True

            # ======================
            # KEEP ACTIVE
            # ======================

            if not closed:

                active_trades.append(
                    trade
                )

        except Exception as e:

            print(
                f"Trade Error: {e}"
            )

            active_trades.append(
                trade
            )

    save_trades(
        active_trades
    )

    save_completed_trades(
        completed
    )