import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

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
    
    # Find the table data for Profit & Loss section
    rows = page_soup.select_one('body main section:nth-of-type(5) div:nth-of-type(3)').find_all('tr')
    
    # Initialize lists to store the table data
    headers = []
    data = []

    for i, row in enumerate(rows):
        cols = [col.text.strip() for col in row.find_all('td')]
        if i == 0:
            headers = cols  # Store headers
        else:
            data.append(cols)  # Store data rows

    # Create DataFrame from the collected data
    df = pd.DataFrame(data, columns=headers)

    # Print the DataFrame to check if data is correct
    print(df)
else:
    print("Login failed!")
