# Get Spot Account Balances
AccessKeyId = ['ACCESS_KEY']
SecretKey = ['SECRET_KEY']
timestamp = str(datetime.utcnow().isoformat())[0:19]
params = urlencode({'AccessKeyId': AccessKeyId,
                    'SignatureMethod': 'HmacSHA256',
                    'SignatureVersion': '2',
                    'Timestamp': timestamp
                   })
method = 'GET'
endpoint = '/v1/account/accounts/3990224/balance'
base_uri = 'api.huobi.pro'
pre_signed_text = method + '\n' + base_uri + '\n' + endpoint + '\n' + params
hash_code = hmac.new(SecretKey.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})
url = 'https://' + base_uri + endpoint + '?' + params + '&' + signature
response = requests.request(method, url)
accts = json.loads(response.text)
print(accts)
