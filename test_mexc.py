import requests

url = "https://contract.mexc.com/api/v1/contract/ticker/BTC_USDT"

try:

    response = requests.get(
        url,
        timeout=10
    )

    print(response.status_code)

    print(response.text[:200])

except Exception as e:

    print(e)