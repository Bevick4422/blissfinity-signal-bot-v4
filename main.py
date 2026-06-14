import asyncio

from config import (
    SYMBOLS,
    TREND_TIMEFRAME,
    ENTRY_TIMEFRAME,
    MAX_SIGNALS
)

from scanner import (
    get_market_data
)

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

from trade_tracker import (
    check_trades
)

from telegram_sender import (
    send_message
)


async def main():

    print("V4 BOT STARTED")

    try:

        await send_message(
            "✅ Blissfinity V4 Online"
        )

    except Exception as e:

        print(
            f"Telegram Error: {e}"
        )

    while True:

        try:

            signal_history = load_signals()

            trades = load_trades()

            signals_sent = 0

            for symbol in SYMBOLS:

                if signals_sent >= MAX_SIGNALS:

                    print(
                        "Max signals reached"
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

                signal = None

                if (
                    bullish_structure(trend_df)
                    and
                    bullish_setup(entry_df)
                ):

                    signal = "LONG"

                elif (
                    bearish_structure(trend_df)
                    and
                    bearish_setup(entry_df)
                ):

                    signal = "SHORT"

                if signal is None:
                    continue

                if (
                    signal_history.get(symbol)
                    == signal
                ):

                    print(
                        f"{symbol} already sent"
                    )

                    continue

                existing_trade = any(

                    trade["pair"] == symbol

                    and

                    not trade["tp2_hit"]

                    and

                    not trade["sl_hit"]

                    for trade in trades

                )

                if existing_trade:

                    print(
                        f"{symbol} already active"
                    )

                    continue

                price = round(
                    float(
                        entry_df["close"].iloc[-1]
                    ),
                    4
                )

                await send_message(
                    f"🚀 {symbol} {signal}"
                )

                signals_sent += 1

                signal_history[symbol] = signal

                save_signals(
                    signal_history
                )

                if signal == "LONG":

                    trades.append({

                        "pair": symbol,
                        "direction": "LONG",

                        "entry": price,

                        "tp1": round(
                            price * 1.05,
                            4
                        ),

                        "tp2": round(
                            price * 1.10,
                            4
                        ),

                        "sl": round(
                            price * 0.95,
                            4
                        ),

                        "tp1_hit": False,
                        "tp2_hit": False,
                        "sl_hit": False

                    })

                else:

                    trades.append({

                        "pair": symbol,
                        "direction": "SHORT",

                        "entry": price,

                        "tp1": round(
                            price * 0.95,
                            4
                        ),

                        "tp2": round(
                            price * 0.90,
                            4
                        ),

                        "sl": round(
                            price * 1.05,
                            4
                        ),

                        "tp1_hit": False,
                        "tp2_hit": False,
                        "sl_hit": False

                    })

                save_trades(
                    trades
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

    asyncio.run(
        main()
    )