#!/bin/sh

VAULT_ADDR='http://localhost:8200'
VAULT_TOKEN='abcd1234'

username=$(curl -s -H "X-Vault-Token: $VAULT_TOKEN" -X GET $VAULT_ADDR/v1/secret/data/myapp | jq -r '.data.data.username')
password=$(curl -s -H "X-Vault-Token: $VAULT_TOKEN" -X GET $VAULT_ADDR/v1/secret/data/myapp | jq -r '.data.data.password')

echo "Username: $username"
echo "Password: $password"