import pandas as pd
from bs4 import BeautifulSoup
import requests

# Function to parse the data from the table
def parse_table(soup):
    # Find the "Profit & Loss" section
    profit_loss_section = soup.find('h2', string="Profit & Loss")
    
    if profit_loss_section:
        table = profit_loss_section.find_next('table')
        
        if table:
            # Extract table headers
            headers = [header.get_text(strip=True) for header in table.find_all('th')]
            
            # Ensure headers are correctly handled
            print(f"Headers: {headers}")

            # Extract table rows
            data = []
            rows = table.find_all('tr')
            for row in rows:
                columns = [col.get_text(strip=True) for col in row.find_all('td')]
                if columns:
                    data.append(columns)
            
            # Ensure data is correctly handled
            print(f"Data: {data}")

            # Create DataFrame
            df = pd.DataFrame(data, columns=headers)
            return df
        else:
            print("Table not found in Profit & Loss section!")
            return None
    else:
        print("Profit & Loss section not found!")
        return None

# Example usage
url = "https://www.screener.in/company/RELIANCE/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

df = parse_table(soup)
if df is not None:
    print(df)
