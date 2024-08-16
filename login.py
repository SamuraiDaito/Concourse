resources:
  - name: getappdata
    type: git
    source:
      uri: "https://github.com/SamuraiDaito/Concourse.git"
      branch: main

jobs:
  - name: fetch-secrets-and-run-script
    plan:
      - get: getappdata
        trigger: true

      - task: fetch-secrets
        config:
          platform: linux
          image_resource:
            type: docker-image
            source:
              repository: hashicorp/vault
              tag: latest
          outputs:
            - name: secrets-output
          run:
            path: sh
            args:
              - -c
              - |
                # Set Vault address and token
                export VAULT_ADDR='http://192.168.3.109:8200'
                export VAULT_TOKEN='abcd1234'
               
                # Fetch secrets from Vault
                Email=$(vault kv get -field=Email secret/screener)
                Password=$(vault kv get -field=Password secret/screener)

                # Print the secrets
                echo "Email: $Email"
                echo "Password: $Password"

                # Export credentials for use in the next task
                echo "EMAIL=$Email" > secrets-output/secrets.sh
                echo "PASSWORD=$Password" >> secrets-output/secrets.sh
                chmod +x secrets-output/secrets.sh

                # List content of directory
                ls -l secrets-output

                # Print content of secrets file
                echo "Contents of file:"
                cat secrets-output/secrets.sh

      - task: run-login-script
        config:
          platform: linux
          image_resource:
            type: docker-image
            source:
              repository: python
              tag: 3.9
          inputs:
            - name: getappdata
            - name: secrets-output
          run:
            path: sh
            args:
              - -c
              - |
                # Install dependencies
                pip install beautifulsoup4 requests

                # Source the secrets.sh file to load environment variables
                source secrets-output/secrets.sh

                # Run the login script
                python getappdata/login.py
