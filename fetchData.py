from bs4 import BeautifulSoup
import json

def extract_stock_data(html_content):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table containing the stock data
    table = soup.find('table')
    
    if not table:
        return []

    # Get all the rows in the table
    rows = table.find_all('tr')
    
    stocks = []
    
    # Loop through each row and extract stock data
    for row in rows[1:]:  # Skipping the header row
        columns = row.find_all('td')
        if len(columns) >= 2:
            stock_number= columns[0].get_text().strip()
            stock_symbol = columns[1].get_text().strip()
            stock_name = columns[2].get_text().strip()
            stocks.append((stock_number, stock_symbol, stock_name))
    
    return stocks

if __name__ == "__main__":
    with open('content.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    stocks_list = extract_stock_data(html_content)
    sorted_list = sorted(stocks_list, key=lambda x: x[1])

    # Save the extracted stock data to a JSON file
    with open('stocks.json', 'w', encoding='utf-8') as file:
        json.dump([{'symbol': stock_symbol, 'name': stock_name} for _, stock_symbol, stock_name in sorted_list], file, ensure_ascii=False, indent=4)

    for stock_number, stock_symbol, stock_name in sorted_list:
        print(f"Num: {stock_number}, Symbol: {stock_symbol}, Name: {stock_name}")

