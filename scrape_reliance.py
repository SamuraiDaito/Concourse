import os
import requests
from bs4 import BeautifulSoup
import webbrowser

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
    # Open the dashboard in the default web browser (optional)
    # webbrowser.open(login_response.url)
    
    # Navigate to the Reliance company page
    reliance_url = "https://www.screener.in/company/RELIANCE/consolidated/"
    reliance_response = session.get(reliance_url)
    reliance_soup = BeautifulSoup(reliance_response.text, 'html.parser')
    
    # Extract Profit & Loss data
    # You may need to adjust the selectors based on the page structure
    pnl_section = reliance_soup.find('div', {'id': 'profit-loss'})
    if pnl_section:
        print("Profit & Loss Data for Reliance:")
        print(pnl_section.get_text())
    else:
        print("Profit & Loss section not found.")
else:
    print("Login failed!")
