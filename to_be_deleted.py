import os
from binance.client import Client

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client = Client(api_key, api_secret)
depth = client.get_order_book(symbol='BNBBTC')
print(depth)