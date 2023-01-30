!pip install binance-connector

import requests
import json
import time
from binance.spot import Spot

url = 'https://api.binance.com/'
client = Spot(key='KEY', secret='SECRET')

# response = client.my_trades(symbol= 'BNBETH', fromId=0, limit = 1000)
# end = len(response) - 1
# print(response[0])
# print(response[end]['id'])

id = 0
n = 0
length = 1000

while length == 1000:
    response = client.my_trades(symbol= 'GALAUSDT', fromId=id, limit = 1000)
    end = len(response) - 1
    id = response[end]['id'] + 1
    length = len(response)
    n += length
    print(n)
    time.sleep(2)
