import jwt
import time 
import sys
import requests
import json
# Get PEM file path
if len(sys.argv) > 1:
    pem = sys.argv[1]
else:
    pem = input("Enter path of private PEM file: ")    

# Open PEM
with open(pem, 'r') as pem_file:
    signing_key = pem_file.read()
    
payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 600, 
    # GitHub App's identifier
    'iss': '278216' 
}
    
# Create JWT
encoded_jwt = jwt.encode(payload, signing_key, algorithm='RS256')

# get installations
get_installs_api_url = "https://api.github.com/app/installations"
get_installs_headers = {"Authorization": "Bearer "+encoded_jwt,"Accept": "application/vnd.github+json"}
get_installs_resp_raw = requests.get(get_installs_api_url, headers=get_installs_headers)

#get token url from installations
get_installs_resp = get_installs_resp_raw.json()
gh_app_token_url = get_installs_resp[0]['access_tokens_url']

#create token
gh_token_resp_raw = requests.post(gh_app_token_url,headers=get_installs_headers)
gh_token_resp = gh_token_resp_raw.json()
gh_token = gh_token_resp['token']

print(gh_token)
