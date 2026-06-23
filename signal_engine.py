def bullish_structure(df):

    try:

        latest_close = df["close"].iloc[-1]

        previous_high = (
            df["high"]
            .iloc[-20:-1]
            .max()
        )

        return latest_close > previous_high

    except:

        return False


def bearish_structure(df):

    try:

        latest_close = df["close"].iloc[-1]

        previous_low = (
            df["low"]
            .iloc[-20:-1]
            .min()
        )

        return latest_close < previous_low

    except:

        return False


def bullish_setup(df):

    try:

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

        move = recent_high - recent_low

        pullback_zone = (
            recent_high - move * 0.50
        )

        return (

            current > pullback_zone

            and

            current < recent_high

        )

    except:

        return False


def bearish_setup(df):

    try:

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

        move = recent_high - recent_low

        pullback_zone = (
            recent_low + move * 0.50
        )

        return (

            current < pullback_zone

            and

            current > recent_low

        )

    except:

        return False