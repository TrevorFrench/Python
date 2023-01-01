import time
import hmac
import requests

base = 'https://ftx.us'      # URL root
path = '/api/nft/balances'   # API endpoint beginning with /api and including all necessary parameters
method = 'GET'               # HTTP method in uppercase (e.g. GET or POST)
key = '[KEY]'                # API KEY
secret = '[SECRET]'          # API SECRET
url = base + path            # base plus path combined to form full URL

ts = int(time.time() * 1000)

signature_payload = f'{ts}{method}{path}'.encode()
signature = hmac.new(secret.encode(), signature_payload, 'sha256').hexdigest()

head = {
    # Only include line if you want to access a subaccount.
    # Remember to URI-encode the subaccount name if it contains special characters!
    # 'FTXUS-SUBACCOUNT': 'my_subaccount_nickname',
    'FTXUS-KEY': key,
    'FTXUS-SIGN': signature,
    'FTXUS-TS': str(ts)
    }

resp = requests.get(url, headers = head)

print(resp.text)
