import os
import requests
from bs4 import BeautifulSoup

# Load credentials from environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Debugging: Print loaded credentials (for debugging)
print(f"Loaded Email: {email}")
print(f"Loaded Password: {password}")

# Additional Debugging: Print all environment variables
print(f"All environment variables: {os.environ}")

if not email or not password:
    print("Email or Password is missing. Exiting...")
    exit(1)

# Use requests to log in to Screener.in
login_url = "https://www.screener.in/login/"
session = requests.Session()
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Identify the correct login form fields from the page source
# Assuming they are "username" and "password", adjust if necessary
login_data = {
    "username": email,
    "password": password
}

# Post the login data to the form
login_response = session.post(login_url, data=login_data)

# Check if login was successful
if login_response.url == "https://www.screener.in/":
    print("Login successful!")
else:
    print("Login failed!")
