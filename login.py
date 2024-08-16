import os
import requests
from bs4 import BeautifulSoup

# Load credentials from environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Debugging: Print loaded credentials (for debugging)
print(f"Loaded Email: {email}")
print(f"Loaded Password: {password}")

# Use requests to log in to Screener.in
login_url = "https://www.screener.in/login/"
session = requests.Session()

# Get the login page first to retrieve any necessary tokens
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Assuming the site uses a CSRF token (this is an example, adjust based on actual form)
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

# Debugging: Print the CSRF token
print(f"CSRF Token: {csrf_token}")

# Assuming the form fields are "username" and "password"
login_data = {
    "username": email,
    "password": password,
    "csrfmiddlewaretoken": csrf_token  # Include the CSRF token if required
}

# Post the login data to the form
login_response = session.post(login_url, data=login_data, headers={"Referer": login_url})

# Debugging: Print the response URL and any error messages
print(f"Response URL: {login_response.url}")
print(f"Response Text: {login_response.text[:500]}")  # Print the first 500 characters of the response

# Check if login was successful
if "dashboard" in login_response.url:  # Adjust this based on the actual successful login URL
    print("Login successful!")
else:
    print("Login failed!")
