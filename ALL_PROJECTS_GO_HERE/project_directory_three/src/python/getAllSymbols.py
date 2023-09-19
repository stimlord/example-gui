import requests

MARKET_TYPES = {
    "spot": "https://api.binance.com/api/v3/exchangeInfo",
    "coinm": "https://dapi.binance.com/dapi/v1/exchangeInfo",
    "usdm": "https://fapi.binance.com/fapi/v1/exchangeInfo"
}

def get_all_symbols(market_type):
    try:
        response = requests.get(MARKET_TYPES[market_type])
        response.raise_for_status()
        data = response.json()
        symbols = []

        if market_type == "spot":
            symbols = [symbol['symbol'] for symbol in data['symbols'] if 'status' in symbol and symbol['status'] == 'TRADING']
        elif market_type == "usdm":
            symbols = [symbol['symbol'] for symbol in data['symbols'] if 'status' in symbol and symbol['status'] == 'TRADING' and symbol['contractType'] == 'PERPETUAL']
        elif market_type == "coinm":
            symbols = [symbol['symbol'] for symbol in data['symbols'] if 'contractStatus' in symbol and symbol['contractStatus'] == 'TRADING']

        print(f"Total symbols for {market_type}: {len(symbols)}")
        print(f"All symbols for {market_type}: {symbols}")

        return symbols

    except requests.RequestException as e:
        print(f"Error fetching symbols for {market_type}: {e}")
        return []
    except KeyError as e:
        print(f"KeyError encountered while fetching symbols for {market_type}. Data: {data}")
        return []

if __name__ == "__main__":
    get_all_symbols("usdm")
    get_all_symbols("coinm")
