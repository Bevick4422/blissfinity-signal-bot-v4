from trade_tracker import (
    load_trades,
    save_trades
)

trades = load_trades()

trade = trades[0]

if not trade["tp1_hit"]:

    print("TP1 HIT SENT")

    trade["tp1_hit"] = True

    save_trades(trades)

else:

    print("TP1 ALREADY SENT")