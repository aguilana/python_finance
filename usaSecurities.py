import requests
from bs4 import BeautifulSoup

BASE_URL = "https://stockanalysis.com/list/nyse-stocks"

def fetch_usa_securities():
    stocks = []
    
    # Loop through pages 1 to 3
    for page in range(1, 4):
        url = f"{BASE_URL}"  # Adapt this pagination URL structure if necessary
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch the page {page}.")

        soup = BeautifulSoup(response.text, 'html.parser')
    
        # Find each row of stock data within the table body
        stock_rows = soup.select("#main-table tbody tr")

        for row in stock_rows:
            # Extract the stock symbol and name
            symbol_elem = row.select_one(".sym a")
            name_elem = row.select_one(".slw")

            symbol = symbol_elem.text.strip() if symbol_elem else None
            name = name_elem.text.strip() if name_elem else None

            # Append the symbol and name to our stocks list
            if symbol and name:
                stocks.append((symbol, name))
                
    return stocks

# Fetch stocks
usa_stocks = fetch_usa_securities()

# Sort the stocks alphabetically by name
sorted_stocks = sorted(usa_stocks, key=lambda x: x[1])  # Sorting by name this time

# Print length of stock list
print(len(usa_stocks))

# Print unique and sorted stocks
# for symbol, name in usa_stocks:
#     print(f"{symbol}: {name}")
