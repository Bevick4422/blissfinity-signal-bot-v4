import requests
import pandas as pd


VALID_INTERVALS = {

    "Min1",
    "Min5",
    "Min15",
    "Min30",
    "Min60",

    "Hour4",
    "Hour8",

    "Day1",

    "Week1",

    "Month1"

}


def get_klines(
    symbol,
    timeframe,
    limit=100
):

    try:

        if timeframe not in VALID_INTERVALS:

            print(
                f"{symbol} invalid timeframe"
            )

            return None

        url = (
            f"https://contract.mexc.com/api/v1/contract/kline/{symbol}"
            f"?interval={timeframe}"
        )

        response = requests.get(
            url,
            timeout=15
        )

        if response.status_code != 200:

            print(
                f"{symbol} HTTP {response.status_code}"
            )

            return None

        data = response.json()

        if data.get("success") is False:

            print(
                f"{symbol} API error"
            )

            return None

        candles = data.get("data")

        if not candles:

            print(
                f"{symbol} empty candles"
            )

            return None

        df = pd.DataFrame({

            "open": candles["open"],
            "high": candles["high"],
            "low": candles["low"],
            "close": candles["close"]

        })

        df = df.astype(float)

        if len(df) < 20:

            print(
                f"{symbol} insufficient candles"
            )

            return None

        return df.tail(limit)

    except Exception as e:

        print(
            f"{symbol} scanner error: {e}"
        )

        return None


def get_market_data(
    symbol,
    trend_tf,
    entry_tf
):

    try:

        trend_df = get_klines(
            symbol,
            trend_tf
        )

        entry_df = get_klines(
            symbol,
            entry_tf
        )

        if trend_df is None:

            return None, None

        if entry_df is None:

            return None, None

        return (
            trend_df,
            entry_df
        )

    except Exception as e:

        print(
            f"{symbol} market data error: {e}"
        )

        return None, None