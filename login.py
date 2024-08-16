import os
import requests
from bs4 import BeautifulSoup

# Load credentials from environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Use requests to log in to Screener.in
login_url = "https://www.screener.in/login/"
session = requests.Session()

# Get the login page first to retrieve any necessary tokens
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the CSRF token
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

# Assuming the form fields are "username" and "password"
login_data = {
    "username": email,
    "password": password,
    "csrfmiddlewaretoken": csrf_token  # Include the CSRF token
}

# Post the login data to the form
login_response = session.post(login_url, data=login_data, headers={"Referer": login_url})

# Check if login was successful by accessing a page that requires login
dashboard_url = "https://www.screener.in/dash/"
dashboard_response = session.get(dashboard_url)
dashboard_soup = BeautifulSoup(dashboard_response.text, 'html.parser')

# Check if the page contains specific content that is only visible after login
if "Core Watchlist feed" in dashboard_response.text:
    print("Login successful!")
else:
    print("Login failed!")

# Optionally, print the entire page content for debugging
print(dashboard_response.text)
