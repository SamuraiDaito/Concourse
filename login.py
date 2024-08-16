import requests
from bs4 import BeautifulSoup
import os

# Fetch credentials from environment variables
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

# URL for login
login_url = 'https://www.screener.in/login/'

# Create a session to persist login cookies
session = requests.Session()

# Fetch the login page
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the form data
# Adjust the selectors according to the actual form on the site
payload = {
    'email': email,
    'password': password
}

# Post the login form
response = session.post(login_url, data=payload)

# Check if login was successful
if 'login' in response.url:
    print("Login failed!")
else:
    print("Login successful!")
