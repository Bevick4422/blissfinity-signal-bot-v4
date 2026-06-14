from price_fetcher import get_price

price = get_price(
    "BTC_USDT"
)

print(
    f"Current BTC Price: {price}"
)

trade = {
    "pair": "BTC_USDT",
    "direction": "LONG",
    "entry": 63000,
    "tp1": 63500,
    "tp2": 64000,
    "sl": 62000
}

if price >= trade["tp1"]:

    print("TP1 HIT")

if price >= trade["tp2"]:

    print("TP2 HIT")

if price <= trade["sl"]:

    print("STOPLOSS HIT")