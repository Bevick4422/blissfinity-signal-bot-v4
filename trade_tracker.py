from trade_storage import (
    load_trades,
    save_trades
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

    changed = False

    for trade in trades:

        price = get_price(
            trade["pair"]
        )

        if price is None:
            continue

        # ==========================
        # LONG TRADES
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
                changed = True

            if (
                not trade["tp2_hit"]
                and price >= trade["tp2"]
            ):

                await send_message(
    f"🚀 TP2 HIT\n\n{trade['pair']}"
)

                trade["tp2_hit"] = True
                changed = True

            if (
                not trade["sl_hit"]
                and price <= trade["sl"]
            ):

                await send_message(
    f"🛑 STOPLOSS HIT\n\n{trade['pair']}"
)

                trade["sl_hit"] = True
                changed = True

        # ==========================
        # SHORT TRADES
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
                changed = True

            if (
                not trade["tp2_hit"]
                and price <= trade["tp2"]
            ):

                await send_message(
                    f"🚀 TP2 HIT\n\n{trade['pair']}"
                )

                trade["tp2_hit"] = True
                changed = True

            if (
                not trade["sl_hit"]
                and price >= trade["sl"]
            ):

                await send_message(
                    f"🛑 STOPLOSS HIT\n\n{trade['pair']}"
                )

                trade["sl_hit"] = True
                changed = True

    if changed:

        save_trades(
            trades
        )