import requests
import os
from binance.client import Client
from time import sleep
import json
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client = Client('api_key', 'api_secret')

is_next_operation_buy = True

DIP_THRESHOLD = 2.50
UPWARD_TREND_THRESHOLD = 2.50
PROFIT_THRESHOLD = 1.25
STOP_LOSS_THRESHOLD = -2.00

btc_balance = client.get_asset_balance(asset='BTC')
mkt_price = client.get_symbol_ticker(symbol='BTCUSDT')


def place_sell_order():
    amount_to_sell = 0.5 * btc_balance
    sell_order = client.create_test_order(symbol='BTCUSDT', side='SELL', type='MARKET', quantity=amount_to_sell)
    return sell_order


def place_buy_order():
    amount_to_buy = 0.73 * btc_balance
    buy_order = client.create_test_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity=amount_to_buy)
    return buy_order


# optional but useful to confirm operations made
def get_operation_details(operation_id):
    operation_details = requests.get('')
    return operation_details


def start_bot():
    while 1:
        attempt_to_make_trade()
        sleep(47)


last_op_price = 500.0


def attempt_to_make_trade():
    current_price = mkt_price
    # noinspection PyTypeChecker
    percentage_diff = (current_price - last_op_price) / last_op_price * 100
    if is_next_operation_buy:
        try_to_buy(percentage_diff)
    else:
        try_to_sell(percentage_diff)


def try_to_buy(percentage_diff):
    if percentage_diff >= UPWARD_TREND_THRESHOLD or percentage_diff <= DIP_THRESHOLD:
        last_op_price = place_buy_order()
        is_next_operation_buy = False


def try_to_sell(percentage_diff):
    if percentage_diff >= PROFIT_THRESHOLD or percentage_diff <= STOP_LOSS_THRESHOLD:
        last_op_price = place_sell_order()
        is_next_operation_buy = True


# Log of the bot
def create_log(msg):
    print(msg)
