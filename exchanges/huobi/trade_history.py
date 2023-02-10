from datetime import datetime
import requests
import json
import hmac
import hashlib
import base64
from urllib.parse import urlencode
import time
import pandas as pd

#Get Trade History (outputs JSON and CSV)
AccessKeyId = ['ACCESS_KEY']
SecretKey = ['SECRET_KEY']
timestamp = str(datetime.utcnow().isoformat())[0:19]
params = urlencode({'AccessKeyId': AccessKeyId,
                    'SignatureMethod': 'HmacSHA256',
                    'SignatureVersion': '2',
                    'Timestamp': timestamp,
                    'account-id': 3990224
                   })
method = 'GET'
endpoint = '/v1/account/history'
base_uri = 'api.huobi.pro'
pre_signed_text = method + '\n' + base_uri + '\n' + endpoint + '\n' + params
hash_code = hmac.new(SecretKey.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})
url = 'https://' + base_uri + endpoint + '?' + params + '&' + signature
response = requests.request(method, url)
txns = json.loads(response.text)

output = []

account = []
currency = []
record = []
transact_amt = []
transact_type = []
avail_balance = []
acct_balance = []
transact_time = []

for item in txns['data']:
    output.append(item)
    account.append(item['account-id'])
    currency.append(item['currency'])
    record.append(item['record-id'])
    transact_amt.append(item['transact-amt'])
    transact_type.append(item['transact-type'])
    avail_balance.append(item['avail-balance'])
    acct_balance.append(item['acct-balance'])
    transact_time.append(item['transact-time'])

print(len(txns['data']))
key = 'next-id'

while key in txns:
    print(txns['next-id'])
    params = urlencode({'AccessKeyId': AccessKeyId,
                        'SignatureMethod': 'HmacSHA256',
                        'SignatureVersion': '2',
                        'Timestamp': timestamp,
                        'account-id': 3990224,
                        'from-id': txns['next-id']
                    })
    method = 'GET'
    endpoint = '/v1/account/history'
    base_uri = 'api.huobi.pro'
    pre_signed_text = method + '\n' + base_uri + '\n' + endpoint + '\n' + params
    hash_code = hmac.new(SecretKey.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
    signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})
    url = 'https://' + base_uri + endpoint + '?' + params + '&' + signature
    response = requests.request(method, url)
    txns = json.loads(response.text)
    print(len(txns['data']))
    for item in txns['data']:
        output.append(item)
        account.append(item['account-id'])
        currency.append(item['currency'])
        record.append(item['record-id'])
        transact_amt.append(item['transact-amt'])
        transact_type.append(item['transact-type'])
        avail_balance.append(item['avail-balance'])
        acct_balance.append(item['acct-balance'])
        transact_time.append(item['transact-time'])
    time.sleep(1)

print(len(output))
df = pd.DataFrame()
df['account'] = account
df['currency'] = currency
df['record'] = record
df['transact_amt'] = transact_amt
df['transact_type'] = transact_type
df['avail_balance'] = avail_balance
df['acct_balance'] = acct_balance
df['transact_time'] = transact_time

df.to_csv('huobi_output.csv')
with open('[FILEPATH]', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
