import requests
from bs4 import BeautifulSoup

BASE_URL = "https://markets.businessinsider.com/index/components/dow_jones"

def fetch_dow_jones_stocks():
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        raise ValueError("Failed to fetch the page.")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    stocks = []

    # Find each row of stock data within the table body
    stock_rows = soup.select(".table__tbody tr")

    for row in stock_rows:
        # Extract the stock name from the first cell of the row
        name_elem = row.select_one(".table__td--big a")
        name = name_elem.text.strip() if name_elem else None

        # Extract the latest price from the second cell of the row (before the <br> tag)
        price_elem = row.select_one(".table__td:nth-of-type(2)")
        price = price_elem.contents[0].strip() if price_elem else None

        # Append the name and price to our stocks list
        if name and price:
            stocks.append((name, price))
        
    return stocks


SP_BASE_URL = "https://markets.businessinsider.com/index/components/s&p_500"

def fetch_sp500_stocks():
    stocks = []

    # Loop through pages 1 to 10
    for page in range(1, 11):
        url = f"{SP_BASE_URL}?p={page}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch the page {page}.")

        soup = BeautifulSoup(response.text, 'html.parser')
    
        # Find each row of stock data within the table body
        stock_rows = soup.select(".table__tbody tr")

        for row in stock_rows:
            # Extract the stock name from the first cell of the row
            name_elem = row.select_one(".table__td--big a")
            name = name_elem.text.strip() if name_elem else None

            # Extract the latest price from the second cell of the row (before the <br> tag)
            price_elem = row.select_one(".table__td:nth-of-type(2)")
            price = price_elem.contents[0].strip() if price_elem else None

            # Append the name and price to our stocks list
            if name and price:
                stocks.append((name, price))
                
    return stocks


dow_stocks = fetch_dow_jones_stocks()
sp500_stocks = fetch_sp500_stocks()

all_stocks = dow_stocks + sp500_stocks

unique_stocks = list(set(all_stocks))

# Sort the stocks alphabetically by name
sorted_stocks = sorted(unique_stocks, key=lambda x: x[0])

# print the length of the list
print(len(sorted_stocks))

# Print unique and sorted stocks
for name, price in sorted_stocks:
    print(f"{name}: ${price}")
