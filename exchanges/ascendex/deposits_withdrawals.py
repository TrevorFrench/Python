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
api_path = 'wallet/transactions'
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

id_list = []
time_list = []
asset_list = []
type_list = []
amount_list = []
commission_list = []
network_id_list = []
status_list = []
num_confirmed_list = []
num_comfirmations_list = []
dest_list = []

has_next = True
page = 1

while has_next == True:
    url = "https://ascendex.com/api/pro/v1/wallet/transactions?pageSize=50&page=" + str(page)
    response = requests.get(url, headers=headers)

    print(response.text)

    data = json.loads(response.text)

    for item in data['data']['data']:
        id_list.append(item['requestId'])
        time_list.append(item['time'])
        asset_list.append(item['asset'])
        type_list.append(item['transactionType'])
        amount_list.append(item['amount'])
        commission_list.append(item['commission'])
        network_id_list.append(item['networkTransactionId'])
        status_list.append(item['status'])
        num_confirmed_list.append(item['numConfirmed'])
        num_comfirmations_list.append(item['numConfirmations'])
        dest_list.append(item['destAddress'])

    page = data['data']['page']
    has_next = data['data']['hasNext']
    print(page)
    print(has_next)
    page += 1

df = pd.DataFrame()
df['id'] = id_list
df['time'] = time_list
df['asset'] = asset_list
df['type'] = type_list
df['amount'] = amount_list
df['commission'] = commission_list
df['network_id'] = network_id_list
df['status'] = status_list
df['num_confirmed'] = num_confirmed_list
df['num_confirmations'] = num_comfirmations_list
df['dest'] = dest_list

df.to_csv('ascendex.csv')
