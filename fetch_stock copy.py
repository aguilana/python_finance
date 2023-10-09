import requests
from bs4 import BeautifulSoup
import json
import asyncio
import aiohttp

API_ENDPOINT = "http://localhost:8080/api/stock/update_stock"
MAX_RETRIES = 3
DELAY = 2  # in seconds

async def fetch_stock_price(session, symbol):
    # Base URL for Yahoo Finance page for stocks
    url = f"https://finance.yahoo.com/quote/{symbol}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }  # This user agent is used to avoid potential blocks from the website.
    
    for i in range(MAX_RETRIES):
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    print(f"Error for {symbol}: {response.status}")
                    return None

                page_content = await response.text()
                soup = BeautifulSoup(page_content, "html.parser")

    
    # if response.status_code != 200:
    #     raise ValueError("Failed to fetch the webpage.")

    # soup = BeautifulSoup(response.content, "html.parser")
    
    # Finding the element containing the current price based on its CSS class
    # Note: This can change if Yahoo Finance updates its website layout
        # Finding the element containing the current price based on its tag and attributes
        # Extract name and symbol

            company_name = None
            stock_symbol = None
            volume = None
            name_element = soup.find("h1", class_="D(ib) Fz(18px)")
            print(name_element.text.split(" ("))
            if name_element:
                full_name = name_element.text.split(" (")
                company_name = full_name[0]
                stock_symbol = full_name[1].replace(")", "") if len(full_name) > 1 else None
                print(f'company_name: {company_name}, stock_symbol: {stock_symbol}')

            # Extract volume
            volume_element = soup.find("fin-streamer", {"data-symbol": symbol, "data-field": "regularMarketVolume"})
            volume = volume_element.text.replace(",", "") if volume_element else None  # Remove commas for numeric conversion

            price_element = soup.find("fin-streamer", {"data-symbol": symbol, "data-test": "qsp-price"})

            # Extract open and previous close values
            open_element = soup.find("td", {"data-test": "OPEN-value",})
            open_value = open_element.text if open_element else None

            # prev_close_element = soup.find("td", {"data-test": "PREV_CLOSE-value"})
            # prev_close_value = prev_close_element.text if prev_close_element else None

            data = {
                "symbol": symbol,
                "name": company_name,
                "latestPrice": price_element.text if price_element else None,
                "volume": volume,
                "open": open_value,
                # "close": prev_close_value,
                # ... Fetch other fields in the same manner.
            }

            print(f"Data fetched for {symbol}: {data}")
            if data:
                return data
            else:
                raise ValueError("Failed to extract the stock price and data.")
            
            break
    
        except (aiohttp.ClientError, ValueError) as e:
            print(f"Error fetching {symbol}: {e}")
            if i < MAX_RETRIES - 1:  # don't sleep after the last try
                await asyncio.sleep(DELAY)
            else:
                print(f"Failed to fetch {symbol} after {MAX_RETRIES} attempts.")


def read_stocks_from_json():
    with open('stocks.json', 'r') as f:
        stocks = json.load(f)
    return [stock['symbol'] for stock in stocks]

async def main():
    symbols = read_stocks_from_json()
    async with aiohttp.ClientSession() as session:
        tasks = [ fetch_stock_price(session, symbol) for symbol in symbols ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

# if __name__ == "__main__":
#     symbol = input("Enter the stock symbol: ").upper()
#     try:
#         price = fetch_stock_price(symbol)
#         print(f"Current stock price for {symbol}: ${price}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

