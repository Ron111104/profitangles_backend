import requests
from bs4 import BeautifulSoup
import yfinance as yf

def fetch_trending_tickers():
    url = 'https://finance.yahoo.com/trending-tickers'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tickers = []
    # Selecting the relevant rows from the table
    for row in soup.select('table tbody tr'):
        print(row)
        print("row above")
        ticker_element = row.select_one('td:nth-child(1) a')
        if ticker_element:
            symbol = ticker_element.text.strip()
            tickers.append(symbol)
        else:
            print("Ticker element not found for row:", row)

    return tickers

def fetch_ticker_data(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info  # Fetching the ticker info
        
        data.append({
            "symbol": ticker,
            "lastPrice": info.get("regularMarketPrice"), 
            "marketCap": info.get("marketCap"),
            "percentChange": info.get("regularMarketChangePercent"),
        })
    return data

def scrape_trending_data():
    trending_tickers = fetch_trending_tickers()
    return fetch_ticker_data(trending_tickers)

if __name__ == "__main__":
    trending_tickers = fetch_trending_tickers()
    print(f"Trending Tickers: {trending_tickers}")

    ticker_data = fetch_ticker_data(trending_tickers)
    print(ticker_data)
