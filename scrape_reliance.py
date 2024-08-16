import os
import requests
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
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

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

    # Navigate to the Reliance company page
    reliance_url = "https://www.screener.in/company/RIL/"
    reliance_response = session.get(reliance_url)
    reliance_soup = BeautifulSoup(reliance_response.text, 'html.parser')

    # Extract the Profit and Loss table
    pl_table = reliance_soup.find('table', {'class': 'table table-hover'})
    
    if pl_table:
        print("Profit and Loss Table:")
        for row in pl_table.find_all('tr'):
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            print("\t".join(cols))
    else:
        print("Profit and Loss table not found.")
else:
    print("Login failed!")
