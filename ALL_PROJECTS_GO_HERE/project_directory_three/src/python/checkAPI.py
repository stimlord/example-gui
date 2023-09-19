import requests

MARKET_TYPES = {
    "spot": "https://api.binance.com/api/v3/exchangeInfo",
    "coinm": "https://dapi.binance.com/dapi/v1/exchangeInfo",
    "usdm": "https://fapi.binance.com/fapi/v1/exchangeInfo"
}


def check_api_response(market_type):
    response = requests.get(MARKET_TYPES[market_type])
    if response.status_code == 200:
        data = response.json()
        symbols = []
        if market_type == "spot":
            symbols = [symbol['symbol'] for symbol in data['symbols'] if 'status' in symbol and symbol['status'] == 'TRADING']
        else:
            symbols = [symbol['symbol'] for symbol in data['symbols'] if 'status' in symbol and symbol['status'] == 'TRADING' and symbol['contractType'] == 'PERPETUAL']

        print(f"First few symbols for {market_type}: {symbols[:5]}")
    else:
        print(f"Failed to fetch symbols for {market_type}. Status code: {response.status_code}")

if __name__ == "__main__":
    check_api_response("usdm")
    check_api_response("coinm")
