from binance.client import Client

client = Client('FOQB4cg4vMBqFR8qY9fgvf2b8lqxdeBSYYeudYGvThGve6br3VlxrIwcGcfcADfx', 'PakNsgyipkoApcBNZce9i3hcYJvpCkhQ3CwpHgIiZbl1r8nwr6bLW7r4cNXBevF5')

depth = client.get_order_book(symbol='BNBBTC')
print(depth)
withdraws = client.get_withdraw_history(asset='BTC')
print(withdraws)