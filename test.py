import requests
from binance.client import  Client
from time import sleep, strftime
import json
client = Client('api_key', 'api_secret')
is_next_operation_buy = True

DIP_THRESHOLD = 2.50
UPWARD_TREND_THRESHOLD = 2.50
PROFIT_THRESHOLD = 2.20
STOP_LOSS_THRESHOLD = -0.7


def get_balances():
    account_balance = requests.get('')
    return float(account_balance.text)


def get_market_price():
    mkt_price = requests.get('')
    return mkt_price


def place_sell_order():
    balance = get_balances()
    amount_to_sell = 0.5 * balance
    price_at_operation_execution = requests.post('', amount_to_sell)
    return price_at_operation_execution


def place_buy_order():
    balance = get_balances()
    amount_to_buy = 0.73 * balance
    price_at_operation_execution = requests.post('', amount_to_buy)
    return price_at_operation_execution


# optional but useful to confirm operations made
def get_operation_details(operation_id):
    operation_details = requests.get('')
    return operation_details


def start_bot():
    while True:
        attempt_to_make_trade()
        sleep(47)


last_op_price = 500.0


def attempt_to_make_trade():
    current_price = get_market_price()
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
