import pandas as pd
import requests
from bs4 import BeautifulSoup
import psycopg2
import os

# Load credentials from environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Database connection parameters
db_name = "concourse"
db_user = "concourse_user"
db_password = "concourse_pass"
db_host = "192.168.3.109"
db_port = "5432"

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

            # Connect to PostgreSQL
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            cursor = conn.cursor()

            # Create table if not exists
            create_table_query = """
            CREATE TABLE IF NOT EXISTS profit_loss (
                "Year" VARCHAR(255),
                "Sales" VARCHAR(255),
                "Expenses" VARCHAR(255),
                "Operating Profit" VARCHAR(255),
                "OPM %" VARCHAR(255),
                "Other Income" VARCHAR(255),
                "Interest" VARCHAR(255),
                "Depreciation" VARCHAR(255),
                "Profit before tax" VARCHAR(255),
                "Tax %" VARCHAR(255),
                "Net Profit" VARCHAR(255),
                "EPS in Rs" VARCHAR(255),
                "Dividend Payout %" VARCHAR(255)
            );
            """
            cursor.execute(create_table_query)
            conn.commit()

            # Insert data into PostgreSQL
            for i, row in df.iterrows():
                insert_query = """
                INSERT INTO profit_loss ("Year", "Sales", "Expenses", "Operating Profit", "OPM %", "Other Income", 
                                         "Interest", "Depreciation", "Profit before tax", "Tax %", "Net Profit", 
                                         "EPS in Rs", "Dividend Payout %")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, tuple(row))
            conn.commit()

            print("Data inserted into PostgreSQL database successfully.")

            # Close the cursor and connection
            cursor.close()
            conn.close()

        else:
            print("Table not found in Profit & Loss section!")
    else:
        print("Profit & Loss section not found!")
else:
    print("Login failed!")
