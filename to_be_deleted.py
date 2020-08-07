import os
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

api_key = os.environ.get('test_api')
api_secret = os.environ.get('test_secret')
client = Client(api_key, api_secret)  # later will add api keys for test network
# TEST NETWORK
client.API_URL = 'https://testnet.binance.vision/api'
# print(client.get_account())  # gets balances for all assets
# print(client.get_asset_balance(asset='BTC'))  # gets balance of a specific asset
"""RETRIEVING LATEST PRICE FOR BITCOIN"""
btc_price = client.get_symbol_ticker(symbol='BTCUSDT')
print(btc_price)
print(btc_price["price"])  # answer above prints out a dictionary so we can access price directly
"""USING BINANCE WEB SOCKET FOR THE LATEST PRICE"""
btc_price = {'error': False}  # this dictionary will hold our latest price dat


def btc_trade_history(msg):
    """define how to process incoming web socket messages"""
    if msg['e'] != 'error':
        print(msg['c'])
        btc_price['last'] = msg['c']
        btc_price['bid'] = msg['b']
        btc_price['last'] = msg['a']
    else:
        btc_price['error'] = True


# initialize and start the web socket
bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_trade_history)
bsm.start()
# terminating the web socket
bsm.stop_socket(conn_key)

# properly terminate web socket
#reactor.stop()
"""GETTING HISTORICAL BITCOIN DATA IN CSV"""
# valid_intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# get timestamp of earliest date data available
timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1m')
print(timestamp)
