from .logger import log_error
from bs4 import BeautifulSoup
import json
import asyncio
import aiohttp
from utils.conversionFunctions import clean_and_convert, convert_market_cap
from config import API_ENDPOINT, MAX_RETRIES, DELAY

async def fetch_stock_price(session, symbol):
    # Base URL for Yahoo Finance page for stocks
    url = f"https://finance.yahoo.com/quote/{symbol}"
    stock_symbol = None
    
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

            company_name = None
            volume = None
            name_element = soup.find("h1", class_="D(ib) Fz(18px)")
            # print(name_element.text.split(" ("))
            if name_element:
                parts = name_element.text.split(" (")
                
                if len(parts) > 2:  # More than one "(" in the name
                    stock_symbol = parts[-1].replace(")", "")
                    company_name = " (".join(parts[:-1])
                elif len(parts) == 2:  # Just one "(" in the name
                    stock_symbol = parts[1].replace(")", "")
                    company_name = parts[0]
                else:  # No "(" in the name
                    company_name = parts[0]
                    stock_symbol = symbol  # If we can't determine stock_symbol from the name, revert to the provided symbol
                    
                if "." in stock_symbol:
                    stock_symbol = stock_symbol.replace(".", "-")
                
                if not stock_symbol:
                    stock_symbol = symbol
                    log_error('Failed to extract stock symbol for data: %s', data, "{stock_symbol} is now {symbol}")


            # Extract volume
            volume_element = soup.find("fin-streamer", {"data-symbol": symbol, "data-field": "regularMarketVolume"})
            volume = clean_and_convert(volume_element.text) if volume_element else None  # Remove commas for numeric conversion

            price_element = soup.find("fin-streamer", {"data-symbol": symbol, "data-test": "qsp-price"})
            price = clean_and_convert(price_element.text) if price_element else None

            # Extract open and previous close values
            open_element = soup.find("td", {"data-test": "OPEN-value",})
            open_value = clean_and_convert(open_element.text) if open_element else None

            prev_close_element = soup.find("td", {"data-test": "PREV_CLOSE-value"})
            prev_close_value = clean_and_convert(prev_close_element.text) if prev_close_element else None

            market_cap_element = soup.find("td", {"data-test": "MARKET_CAP-value"})
            if market_cap_element:
                market_cap = convert_market_cap(market_cap_element.text)
            else:
                market_cap = None

            high_price = max(price, prev_close_value)
            low_price = min(price, prev_close_value)

            data = {
                "symbol": symbol,
                "name": company_name,
                "latestPrice": price,
                "marketCap": market_cap,
                "volume": volume,
                "open": open_value,
                "close": prev_close_value,
                "high": high_price,
                "low": low_price,

            }

            if data:
                await send_to_node(data)
                return data
            else:
                raise ValueError("Failed to extract the stock price and data.")
            
            break
    
        except (aiohttp.ClientError, ValueError, Exception) as e:
            print(f"Error fetching {stock_symbol}: {e}")
            if i < MAX_RETRIES - 1:  # don't sleep after the last try
                await asyncio.sleep(DELAY)
            else:
                print(f"Failed to fetch {stock_symbol } after {MAX_RETRIES} attempts.")

async def send_to_node(data):
    stock_symbol = data["symbol"]
    url = f'{API_ENDPOINT}{stock_symbol}'
    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=data) as response:
            if response.status != 200:
                error_msg = f"Error sending data for {stock_symbol}. Status: {response.status}"
                print(error_msg)
                log_error(error_msg)
                return None
            return await response.json()

def read_stocks_from_json():
    try:
        with open('stocks.json', 'r') as f:
            stocks = json.load(f)
        return [stock['symbol'].replace(".", "-") for stock in stocks]
    except Exception as e:
        error_msg = f"Error reading stocks from JSON: {e}"
        print(error_msg)
        log_error(error_msg)
        return []  # return an empty list in case of error

async def main():
    symbols = read_stocks_from_json()
    async with aiohttp.ClientSession() as session:
        tasks = [ fetch_stock_price(session, symbol) for symbol in symbols ]
        await asyncio.gather(*tasks)

def run_main():
    # As asyncio.run is an async function, wrap the call to main() inside this function
    asyncio.run(main())