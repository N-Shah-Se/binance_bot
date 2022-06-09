from binance.client import Client

API_KEY = '4M7OecHKUHqpl1dimga3RS5lQblxDqYA4fIWtUg3fVFGierMuQPYUplXKCupAqdo'
SECRET_KEY = 'zgVAKp2doMX3rr3nogl2nSI6TUsdWGJc7kPwbsnUVyp5dkaE2etbuNcZ4tLm4U4C'


client = Client(API_KEY, SECRET_KEY)

from binance.enums import *

symbol='XRPUSDT'
quantity=100
price=0.1000

order = client.create_order(
    symbol=symbol,
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=quantity,
    price=str(price)
    )

print(order)
print('----------')

print(order['symbol'])
print(order['orderId'])
print(order['price'])
print(order['origQty'])
print(order['status'])

print('----------')
print('Cancelling order')
result = client.cancel_order(
    symbol=symbol,
    orderId=order['orderId']
    )

print(result['symbol'])
print(result['orderId'])


print('----------')
print('Order Book')
orders = client.get_all_orders(symbol=order['symbol'])

for i in orders:
    print('----------')
    print(i['symbol'])
    print(i['orderId'])
    print(i['side'])
    print(i['status'])

