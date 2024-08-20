import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import os

# Load credentials from environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Print credentials to verify (remove or comment this in production)
print(f"Email: {email}")
print(f"Password: {password}")

# URL for Reliance company's Profit & Loss page
login_url = "https://www.screener.in/login/"
reliance_url = "https://www.screener.in/company/RELIANCE/"

# Use requests to log in to Screener.in
session = requests.Session()
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract CSRF token
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
if csrf_token:
    csrf_token = csrf_token['value']
    print(f"CSRF Token: {csrf_token}")  # Debugging print
else:
    print("CSRF token not found!")
    exit()

# Prepare login data with the extracted CSRF token
login_data = {
    "username": email,
    "password": password,
    "csrfmiddlewaretoken": csrf_token
}

# Add headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": login_url
}

# Post the login data to the form
login_response = session.post(login_url, data=login_data, headers=headers)

# Print the response to understand what went wrong
print(login_response.text)  # Debugging print

# Check if login was successful
if login_response.url == "https://www.screener.in/dash/":
    print("Login successful!")
    # Proceed with scraping and database insertion...
else:
    print("Login failed!")
