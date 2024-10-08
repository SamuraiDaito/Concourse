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
    reliance_url = "https://www.screener.in/company/RELIANCE/consolidated/"

    # Fetch the page content
    page_response = session.get(reliance_url)
    page_soup = BeautifulSoup(page_response.text, 'html.parser')

    # Debug print to check page content
    # print(page_soup.prettify()[:2000])  # Print first 2000 characters for inspection

    # Find the "Profit & Loss" section
    profit_loss_section = page_soup.find('h2', string="Profit & Loss")

    if profit_loss_section:
        table = profit_loss_section.find_next('table')
        
        if table:
            # Extract table headers
            headers = [header.get_text(strip=True) for header in table.find_all('th')]
            print(f"Headers: {headers}")

            # Extract table rows
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                column_data = [column.get_text(strip=True) for column in columns]
                if column_data:
                    print(column_data)
        else:
            print("Table not found in Profit & Loss section!")
    else:
        print("Profit & Loss section not found!")
else:
    print("Login failed!")
