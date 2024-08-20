import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import psycopg2
from psycopg2 import sql

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
reliance_url = "https://www.screener.in/company/RELIANCE/consolidated/"

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
            headers = ['Parameters'] + [header.get_text(strip=True) for header in table.find_all('th')]
            headers = [header for header in headers if header]  # Remove empty headers
            print(f"Headers: {headers}")

            # Extract table rows
            data = []
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                column_data = [column.get_text(strip=True) for column in columns]
                if column_data:
                    data.append([''] + column_data)  # Add an empty value for 'Parameters'
            
            # Check number of columns in data and headers
            if data:
                num_data_columns = len(data[0])
                num_headers = len(headers)
                print(f"Number of columns in data: {num_data_columns}")
                print(f"Number of headers: {num_headers}")

                # Adjust data if there are extra columns
                if num_data_columns > num_headers:
                    data = [row[:num_headers] for row in data]
                elif num_data_columns < num_headers:
                    headers = headers[:num_data_columns]
                
                # Create a DataFrame
                df = pd.DataFrame(data, columns=headers)
                
                # Connect to PostgreSQL database
                try:
                    conn = psycopg2.connect(
                        dbname=db_name,
                        user=db_user,
                        password=db_password,
                        host=db_host,
                        port=db_port
                    )
                    cursor = conn.cursor()
                    
                    # Create table if it doesn't exist
                    create_table_query = """
                    CREATE TABLE IF NOT EXISTS profit_loss (
                        "Parameters" TEXT,
                        "Mar 2013" TEXT,
                        "Mar 2014" TEXT,
                        "Mar 2015" TEXT,
                        "Mar 2016" TEXT,
                        "Mar 2017" TEXT,
                        "Mar 2018" TEXT,
                        "Mar 2019" TEXT,
                        "Mar 2020" TEXT,
                        "Mar 2021" TEXT,
                        "Mar 2022" TEXT,
                        "Mar 2023" TEXT,
                        "Mar 2024" TEXT,
                        "TTM" TEXT
                    )
                    """
                    cursor.execute(create_table_query)
                    
                    # Remove empty headers from DataFrame
                    headers = [header for header in headers if header]
                    df.columns = headers
                    
                    # Insert data into the table
                    insert_query = sql.SQL("""
                        INSERT INTO profit_loss ({})
                        VALUES ({})
                    """).format(
                        sql.SQL(', ').join(map(sql.Identifier, headers)),
                        sql.SQL(', ').join(sql.Placeholder() * len(headers))
                    )
                    
                    for index, row in df.iterrows():
                        cursor.execute(insert_query, row.tolist())
                    
                    # Commit changes and close the connection
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    print("Data inserted successfully into PostgreSQL!")
                except Exception as e:
                    print(f"Database connection failed: {e}")
        else:
            print("Table not found in Profit & Loss section!")
    else:
        print("Profit & Loss section not found!")
else:
    print("Login failed!")
