import os
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# Load credentials from environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Print loaded credentials (for debugging)
print(f"Loaded Email: {email}")
print(f"Loaded Password: {password}")

# Use requests to log in to Screener.in
login_url = "https://www.screener.in/login/"
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

    # URL for Reliance company's Profit & Loss page
    reliance_url = "https://www.screener.in/company/RELIANCE/"
    
    # Fetch the page content
    page_response = session.get(reliance_url)
    page_soup = BeautifulSoup(page_response.text, 'html.parser')
    
    # Use CSS selector to find the relevant table
    rows = page_soup.select_one('body main section:nth-of-type(5) div:nth-of-type(3)').find_all('tr')
    
    # Extract table data
    table_data = []
    headers = [col.text.strip() for col in rows[0].find_all('th')]  # Extract headers from the first row
    
    for row in rows[1:]:
        cols = [col.text.strip() for col in row.find_all('td')]
        if cols:
            table_data.append(cols)
    
    # Print the table in a formatted view
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
else:
    print("Login failed!")
