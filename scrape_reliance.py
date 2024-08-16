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

        # Replace with the actual URL
        url = 'https://www.screener.in/company/RELIANCE/consolidated/#profit-loss'
        
        # Send an HTTP request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the table with class 'data-table'
            table = soup.find('table', {'class': 'data-table'})
            
            # Extract headers
            headers = [th.text.strip() for th in table.find('thead').find_all('th')]
            
            # Extract rows
            data = []
            for row in table.find('tbody').find_all('tr'):
                columns = row.find_all('td')
                data_row = [col.text.strip() for col in columns]
                data.append(data_row)
            
            # Print headers and data
            print("Headers:", headers)
            for row in data:
                print(row)
        else:
            print("Failed to retrieve the webpage")
    else:
        print("Profit & Loss section not found!")
else:
    print("Login failed!")
