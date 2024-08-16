#!/bin/sh

# Source the credentials
source secrets-output/secrets.sh

# Perform login using curl
curl.exe -X POST "https://www.screener.in/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=$USERNAME&password=$PASSWORD"
