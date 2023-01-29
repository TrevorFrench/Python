import requests
import json
import base64
import hmac
import hashlib
import time
import pandas as pd

milliseconds = str(round(time.time() * 1000))

def hmac_sha256(secret, pre_hash_msg):
    return hmac.new(secret.encode('utf-8'), pre_hash_msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature(secret, api_path, ts):
    pre_hash_msg = f'{ts}+{api_path}'
    print("prehash msg: {}", pre_hash_msg)
    return base64.b64encode(hmac_sha256(secret, pre_hash_msg)).decode('utf-8')

secret = '[SECRET_KEY]'
api_path = 'info'
timestamp = milliseconds

signature = get_signature(secret, api_path, timestamp)

api_key = '[API_KEY]'

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-auth-key": api_key,
    "x-auth-signature": signature,
    "x-auth-timestamp": timestamp
}

url = "https://ascendex.com/api/pro/v1/info"
response = requests.get(url, headers=headers)

print(response.text)
