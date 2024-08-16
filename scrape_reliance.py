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
    
    # URL for Reliance company's Profit & Loss page
    reliance_url = "https://www.screener.in/company/RELIANCE/"
    
    # Fetch the page content
    page_response = session.get(reliance_url)
    page_soup = BeautifulSoup(page_response.text, 'html.parser')
    
    # Find the "Profit & Loss" section
    profit_loss_section = page_soup.find('h2', text="Profit & Loss").find_next('table')
    
    if profit_loss_section:
        # Print the "Profit & Loss" data
        print("Profit & Loss Data for Reliance:")
        print(profit_loss_section.prettify())
    else:
        print("Profit & Loss section not found!")
    
    # Optionally open the Reliance page in a web browser
    webbrowser.open(reliance_url)
else:
    print("Login failed!")
