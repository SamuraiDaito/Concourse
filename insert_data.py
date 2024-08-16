import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import os

# Load credentials from environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# URL for Reliance company's Profit & Loss page
login_url = "https://www.screener.in/login/"
reliance_url = "https://www.screener.in/company/RELIANCE/"

# Use requests to log in to Screener.in
session = requests.Session()
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract CSRF token
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
if csrf_token:
    csrf_token = csrf_token['value']
else:
    print("CSRF token not found!")
    exit()

# Prepare login data with the extracted CSRF token
login_data = {
    "username": email,
    "password": password,
    "csrfmiddlewaretoken": csrf_token
}

# Post the login data to the form
login_response = session.post(login_url, data=login_data, headers={"Referer": login_url})

# Check if login was successful
if login_response.url == "https://www.screener.in/dash/":
    print("Login successful!")

    # Fetch the page content
    page_response = session.get(reliance_url)
    page_soup = BeautifulSoup(page_response.text, 'html.parser')

    # Find the "Profit & Loss" section
    profit_loss_section = page_soup.find('h2', string="Profit & Loss")
    
    if profit_loss_section:
        table = profit_loss_section.find_next('table')
        
        if table:
            # Extract table headers
            headers = [header.get_text(strip=True) for header in table.find_all('th')]
            print(f"Headers: {headers}")
            
            # Extract table rows
            data = []
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                column_data = [column.get_text(strip=True) for column in columns]
                if column_data:
                    data.append(column_data)

            # Create a DataFrame
            df = pd.DataFrame(data, columns=headers)
            # Save DataFrame to CSV
            df.to_csv('profit_loss_data.csv', index=False)
            print("Data saved to profit_loss_data.csv")

            # Database connection details
            DATABASE_URL = 'postgresql://concourse_user:concourse_pass@localhost:5432/concourse'
            
            # Create a SQLAlchemy engine
            engine = create_engine(DATABASE_URL)
            
            # Insert the data into the 'profit_loss' table
            df.to_sql('profit_loss', engine, if_exists='replace', index=False)
            print("Data inserted into PostgreSQL database.")
        else:
            print("Table not found in Profit & Loss section!")
    else:
        print("Profit & Loss section not found!")
else:
    print("Login failed!")
