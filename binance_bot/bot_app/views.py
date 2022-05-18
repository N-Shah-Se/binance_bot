import requests
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
import websocket, json
from binance.exceptions import BinanceAPIException
from binance.client import Client
sell_limit,buy_limit = 0,0
client = None

def on_open(ws):
    # return JsonResponse({"msg": "Connection Oppened"})
    print("Started")


def on_close(ws):
    # return JsonResponse({"msg": "Connection Closes"})
    print("Closed")


def on_error(ws,error):
    print("error")
    return JsonResponse({"msg":f"{error}"})
def order(side, quantity, symbol="FORUSDT"):
    try:
        order_ = client.create_order(symbol=symbol, side=side, type=client.ORDER_TYPE_MARKET, quantity=quantity)
    except BinanceAPIException as ex:
        return JsonResponse({"Failure": f"{ex}"})
    return JsonResponse({"msg": f"{order_}"})

def on_message(ws,message, sell_limit=sell_limit, buy_limit=buy_limit):
    candle_data = json.loads(message)
    closing_rate = float(candle_data['k']['c'])
    if closing_rate >= sell_limit:
        order("SELL", 100)
    elif closing_rate <= buy_limit:
        order("BUY", 100)
#
#
# def on_order():
#     pass

# Create your views here.

@api_view(['POST'])
def start_bot(request):
    api_key = request.data['api_key']
    secret_key = request.data['secret_key']
    print("hellloooooo")
    client = Client(api_key, secret_key)
    sell_limit, buy_limit = 0.055, 0.045
    websocket_app =websocket.WebSocketApp(settings.SOCKET, on_open=on_open, on_close=on_close, on_error=on_error,on_message=on_message)
    websocket_app.run_forever()


#
#     ##### Multiple Operations #####
#
#     def on_open():
#         return JsonResponse({"msg": "Connection Oppened"})
#         # print("Started")
#
#     def on_close():
#         return JsonResponse({"msg": "Connection Closes"})
#         # print("Closed")
#
#     def on_error(error):
#         return JsonResponse({"Error": f"{error}"})
#
#     def order(side, quantity, symbol="FORUSDT"):
#         try:
#             order_ = client.create_order(symbol=symbol, side=side, type=client.ORDER_TYPE_MARKET, quantity=quantity)
#         except BinanceAPIException as ex:
#             return JsonResponse({"Failure": f"{ex}"})
#         return JsonResponse({"msg": f"{order_}"})
#
#     def on_message(message, sell_limit=sell_limit, buy_limit=buy_limit):
#         candle_data = json.loads(message)
#         closing_rate = float(candle_data['k']['c'])
#         if closing_rate >= sell_limit:
#             order("SELL", 100)
#         elif closing_rate <= buy_limit:
#             order("BUY", 100)
#
#     websocket_app =websocket.WebSocketApp(settings.SOCKET, on_open=on_open, on_close=on_close, on_error=on_error,on_message=on_message)
#     websocket_app.run_forever()


# import websocket, json, numpy
# from binance.client import Client
# from binance.enums import *
#
# @api_view(['POST'])
# def bot(request):
#     SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
#     RSI_PERIOD = 14
#     RSI_OVERBOUGHT = 70
#     RSI_OVERSOLD = 30
#     TRADE_SYMBOL = 'ETHUSD'
#     TRADE_QUANTITY = 0.05
#
#     closes = []
#     in_position = False
#     api_key = request.data['api_key']
#     secret_key = request.data['secret_key']
#     client = Client(api_key,secret_key , tld='us')
#
#     def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
#         try:
#             print("sending order")
#             order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
#             print(order)
#         except Exception as e:
#             print("an exception occured - {}".format(e))
#             return False
#         return True
#
#     def on_open(ws):
#         print('opened connection')
#
#     def on_close(ws):
#         print('closed connection')
#
#     def order(side, quantity, symbol="FORUSDT"):
#         try:
#             order_ = client.create_order(symbol=symbol, side=side, type=client.ORDER_TYPE_MARKET, quantity=quantity)
#         except BinanceAPIException as ex:
#             return JsonResponse({"Failure": f"{ex}"})
#         return JsonResponse({"msg": f"{order_}"})
#
#     def on_message(ws, message, sell_limit=sell_limit, buy_limit=buy_limit):
#         candle_data = json.loads(message)
#         closing_rate = float(candle_data['k']['c'])
#         if closing_rate >= sell_limit:
#             order("SELL", 100)
#         elif closing_rate <= buy_limit:
#             order("BUY", 100)
#
#     # def on_message(ws, message):
#     #     global closes, in_position
#     #
#     #     print('received message')
#     #     json_message = json.loads(message)
#     #     # pprint.pprint(json_message)
#     #
#     #     candle = json_message['k']
#     #
#     #     is_candle_closed = candle['x']
#     #     close = candle['c']
#     #
#     #     if is_candle_closed:
#     #         print("candle closed at {}".format(close))
#     #         closes.append(float(close))
#     #         print("closes")
#     #         print(closes)
#     #
#     #         if len(closes) > RSI_PERIOD:
#     #             np_closes = numpy.array(closes)
#     #             # rsi = talib.RSI(np_closes, RSI_PERIOD)
#     #             print("all rsis calculated so far")
#     #             # print(rsi)
#     #             # last_rsi = rsi[-1]
#     #             # print("the current rsi is {}".format(last_rsi))
#     #
#     #             # if last_rsi > RSI_OVERBOUGHT:
#     #             #     if in_position:
#     #             #         print("Overbought! Sell! Sell! Sell!")
#     #             #         # put binance sell logic here
#     #             #         order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
#     #             #         if order_succeeded:
#     #             #             in_position = False
#     #             #     else:
#     #             #         print("It is overbought, but we don't own any. Nothing to do.")
#     #
#     #             # if last_rsi < RSI_OVERSOLD:
#     #             #     if in_position:
#     #             #         print("It is oversold, but you already own it, nothing to do.")
#     #             #     else:
#     #             #         print("Oversold! Buy! Buy! Buy!")
#     #             #         # put binance buy order logic here
#     #             #         order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
#     #             #         if order_succeeded:
#     #             #             in_position = True
#
#     ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
#     ws.run_forever()