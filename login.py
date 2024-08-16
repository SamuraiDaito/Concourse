import requests

# Replace with actual URL and form data for login
login_url = "https://www.screener.in/login/"
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Prepare login payload
payload = {
    'username': email,
    'password': password,
}

# Create a session to persist the login
session = requests.Session()
response = session.post(login_url, data=payload)

if response.ok:
    print("Login successful!")
else:
    print("Login failed!")
