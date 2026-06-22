import pandas as pd


# ========================================
# EMA HELPERS
# ========================================

def add_emas(df):

    df = df.copy()

    df["ema50"] = (
        df["close"]
        .ewm(span=50)
        .mean()
    )

    df["ema200"] = (
        df["close"]
        .ewm(span=200)
        .mean()
    )

    return df


# ========================================
# TREND STRUCTURE
# ========================================

def bullish_structure(df):

    try:

        df = add_emas(df)

        close = df["close"].iloc[-1]

        ema50 = df["ema50"].iloc[-1]

        ema200 = df["ema200"].iloc[-1]

        previous_high = (
            df["high"]
            .iloc[-20:-1]
            .max()
        )

        return (

            close > previous_high

            and

            ema50 > ema200

            and

            close > ema200

        )

    except:

        return False


def bearish_structure(df):

    try:

        df = add_emas(df)

        close = df["close"].iloc[-1]

        ema50 = df["ema50"].iloc[-1]

        ema200 = df["ema200"].iloc[-1]

        previous_low = (
            df["low"]
            .iloc[-20:-1]
            .min()
        )

        return (

            close < previous_low

            and

            ema50 < ema200

            and

            close < ema200

        )

    except:

        return False


# ========================================
# VOLUME FILTER
# ========================================

def strong_volume(df):

    try:

        current_volume = (
            df["volume"]
            .iloc[-1]
        )

        average_volume = (
            df["volume"]
            .iloc[-20:]
            .mean()
        )

        return (
            current_volume >
            average_volume * 1.5
        )

    except:

        return False


# ========================================
# ENTRY SETUPS
# ========================================

def bullish_setup(df):

    try:

        if not strong_volume(df):

            return False

        current = df["close"].iloc[-1]

        recent_high = (
            df["high"]
            .iloc[-20:]
            .max()
        )

        recent_low = (
            df["low"]
            .iloc[-20:]
            .min()
        )

        move = (
            recent_high -
            recent_low
        )

        retracement = (
            recent_high -
            move * 0.5
        )

        return (

            current > retracement

            and

            current < recent_high

        )

    except:

        return False


def bearish_setup(df):

    try:

        if not strong_volume(df):

            return False

        current = df["close"].iloc[-1]

        recent_high = (
            df["high"]
            .iloc[-20:]
            .max()
        )

        recent_low = (
            df["low"]
            .iloc[-20:]
            .min()
        )

        move = (
            recent_high -
            recent_low
        )

        retracement = (
            recent_low +
            move * 0.5
        )

        return (

            current < retracement

            and

            current > recent_low

        )

    except:

        return False