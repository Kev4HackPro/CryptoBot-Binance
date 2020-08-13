"""DEMO BOT FIRST WE TEST TRADING STRATEGIES"""
import json
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import os

test_key = os.environ.get('test_api')
test_secret = os.environ.get('test_secret')
client = Client(test_key, test_secret)

btc_balance = client.get_asset_balance(asset='BTC')

"""Web Socket for latest market prices"""
btc_mkt_price = {'error': False}


def btc_trade_prices(msg):
    if msg['e'] != 'error':
        print(msg['c'])
        btc_mkt_price['last'] = msg['c']
        btc_mkt_price['bid'] = msg['b']
        btc_mkt_price['ask'] = msg['a']


bsm = BinanceSocketManager(client)
# connection_key
# noinspection PyTypeChecker
conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_trade_prices)
bsm.start()

# stopping
bsm.stop_socket(conn_key)
# or
# noinspection PyUnresolvedReferences
reactor.stop()

def place_sell_order():
