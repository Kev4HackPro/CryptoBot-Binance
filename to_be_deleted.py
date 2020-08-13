import os
import csv
import pandas as pd
import json
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
btc_price = {'error': False}  # this dictionary will hold our latest price data


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
# bsm.stop_socket(conn_key)

# properly terminate web socket
# reactor.stop()
"""GETTING HISTORICAL BITCOIN DATA IN CSV"""
# valid_intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# get timestamp of earliest date data available
timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1d')
print(timestamp)
# request historical candle (or klines) data
bars = client.get_historical_klines('BTCUSDT', '1d', timestamp, limit=1000)
# option 1 - save to file using json method
with open('btc_bars.json', 'w') as e:
    json.dump(bars, e)

# option 2 - save as csv file using csv writer library

with open('btc_bars.csv', 'w', newline='') as f:
    wr = csv.writer(f)
    for line in bars:
        wr.writerow(line)

# option 3 - save as CSV file without using a library
with open('btc_bars.csv', 'w') as d:
    for line in bars:
        d.write(f"{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}\n")

# option 4 - Create a pandas DataFrame and export to csv
btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
btc_df.set_index('date', inplace=True)
print(btc_df.head())
# export DataFrame tp csv
btc_df.to_csv('btc_bars3.csv')

