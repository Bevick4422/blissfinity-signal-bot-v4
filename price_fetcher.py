import requests


def get_price(symbol):

    try:

        url = (
            "https://contract.mexc.com/api/v1/contract/ticker"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        if not data.get("success"):
            return None

        for coin in data["data"]:

            if coin["symbol"] == symbol:

                return float(
                    coin["lastPrice"]
                )

        return None

    except Exception as e:

        print(
            f"{symbol} error: {e}"
        )

        return None