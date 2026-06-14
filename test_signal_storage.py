from signal_storage import (
    load_signals,
    save_signals
)

data = load_signals()

print(data)

data["BTC_USDT"] = "LONG"

save_signals(data)

print("saved")