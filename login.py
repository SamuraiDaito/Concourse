import os
import requests
from bs4 import BeautifulSoup

# Read environment variables
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

if not email or not password:
    raise ValueError("EMAIL or PASSWORD environment variables not set")

# Define the URL and payload
login_url = 'https://www.screener.in/login/'
payload = {
    'email': email,
    'password': password
}

# Make the login request
response = requests.post(login_url, data=payload)

# Check if login was successful
if response.ok:
    print("Login successful!")
else:
    print("Login failed!")
    print("Status Code:", response.status_code)
    print("Response:", response.text)

# Debugging: Print response content for further investigation
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.prettify())
