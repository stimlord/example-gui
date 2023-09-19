import os
import zipfile
import requests
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Constants and initializations
BASE_URL = "https://data.binance.vision/data"
STORAGE_PATH = "/Volumes/rawPriceData"
DIRECTORY_STRUCTURE_FILE = os.path.join(STORAGE_PATH, 'directory_structure.json')
MARKET_TYPES = {
    "spot": "https://api.binance.com/api/v3/exchangeInfo",
    "coinm": "https://dapi.binance.com/dapi/v1/exchangeInfo",
    "usdm": "https://fapi.binance.com/fapi/v1/exchangeInfo"
}
MAX_SYMBOL_THREADS = 25

def sync_directory_structure_with_disk():
    # First, initialize the structure from disk
    initialize_directory_structure_from_disk()

    for market, symbols in directory_structure.items():
        for symbol, files in symbols.items():
            for file_name in files:
                csv_file_path = os.path.join(STORAGE_PATH, market, symbol, file_name)
                if not os.path.exists(csv_file_path):
                    directory_structure[market][symbol].remove(file_name)
                    print(f"Removed {file_name} from directory structure as it doesn't exist on disk.")
                elif file_name not in directory_structure[market][symbol]:
                    directory_structure[market][symbol].append(file_name)
                    print(f"Added {file_name} to directory structure as it exists on disk.")

    save_directory_structure(directory_structure)

# Save & Load directory structure
def save_directory_structure(structure):
    with open(DIRECTORY_STRUCTURE_FILE, 'w') as file:
        json.dump(structure, file)

def load_directory_structure():
    if os.path.exists(DIRECTORY_STRUCTURE_FILE):
        with open(DIRECTORY_STRUCTURE_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

# Get all trading symbols
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

# Downloading the trading data
def download_file(symbol, market, year, month):
    csv_file_name = f"{symbol}-trades-{year}-{month}.csv"
    if symbol in directory_structure and csv_file_name in directory_structure[symbol]:
        print(f"CSV data for {symbol} {year}-{month} already exists. Skipping download.")
        return "Data downloaded"

    url = f"{BASE_URL}/{market}/monthly/trades/{symbol}/{symbol}-trades-{year}-{month}.zip"
    zip_file_path = os.path.join(STORAGE_PATH, market, symbol, f"{symbol}-trades-{year}-{month}.zip")
    os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(zip_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {symbol} data for {year}-{month}")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(zip_file_path))
        os.remove(zip_file_path)
        print(f"Extracted and deleted ZIP for {symbol} {year}-{month}")
        if symbol not in directory_structure:
            directory_structure[symbol] = []
        directory_structure[symbol].append(csv_file_name)
        save_directory_structure(directory_structure)
        return "Data downloaded"
    else:
        print(f"No data found for {symbol} {year}-{month}")
        return "No data"

# Main function
def initialize_directory_structure_from_disk():
    for root, _, files in os.walk(STORAGE_PATH):
        for file in files:
            if file.endswith('.csv'):
                symbol = file.split('-trades-')[0]
                if symbol not in directory_structure:
                    directory_structure[symbol] = []
                directory_structure[symbol].append(file)
    # Save the initialized structure to the file
    save_directory_structure(directory_structure)

def process_symbol(symbol, market):
    if market not in directory_structure:
        directory_structure[market] = {}

    if symbol not in directory_structure[market] or not directory_structure[market][symbol]:
        directory_structure[market][symbol] = []
        oldest_year, oldest_month = datetime.now().year, datetime.now().month
        newest_year, newest_month = oldest_year, oldest_month
    else:
        oldest_year, oldest_month = map(int, directory_structure[market][symbol][0].split('-trades-')[1].rsplit('.', 1)[0].split('-'))
        newest_year, newest_month = map(int, directory_structure[market][symbol][-1].split('-trades-')[1].rsplit('.', 1)[0].split('-'))

    # Checking for older data
    while True:
        oldest_month -= 1
        if oldest_month == 0:
            oldest_month = 12
            oldest_year -= 1
        response_message = download_file(symbol, market, str(oldest_year), f"{oldest_month:02}")
        if response_message == "No data":
            break

    # Checking for newer data
    while True:
        newest_month += 1
        if newest_month == 13:
            newest_month = 1
            newest_year += 1
        response_message = download_file(symbol, market, str(newest_year), f"{newest_month:02}")
        if response_message == "No data":
            break


def process_market(market):
    symbols = get_all_symbols(market)

    with ThreadPoolExecutor(max_workers=MAX_SYMBOL_THREADS) as executor:
        list(executor.map(lambda symbol: process_symbol(symbol, market), symbols))

def main():

    # If directory_structure is empty, initialize it from the disk
    if not directory_structure:
        initialize_directory_structure_from_disk()

    # Process each market one at a time
    for market in MARKET_TYPES.keys():
        process_market(market)

directory_structure = load_directory_structure()

if __name__ == "__main__":
    main()
