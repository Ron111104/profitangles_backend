# stocks/utils.py
import requests

def fetch_stock_data(symbol):
    url = f"https://www.google.com/finance/quote/{symbol}"
    response = requests.get(url)
    # Process the response to extract relevant data
    ...
    return data
