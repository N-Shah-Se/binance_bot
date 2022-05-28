import threading

from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, APIView
import websocket, json
from binance.exceptions import BinanceAPIException
from binance.client import Client
import json
from rest_framework import response, permissions
from rest_framework.decorators import permission_classes
import requests
from datetime import datetime
from time import sleep

sell_limit, buy_limit = 0, 0
client = None
from rest_framework.views import APIView
from user_account.views import send_otp
import random


# Create your views here.

class BotOperation(APIView):
    @api_view(['POST'])
    # @permission_classes([permissions.AllowAny])
    def check_credentials(request):
        api_key = request.data['api_key']
        secret_key = request.data['secret_key']
        try:
            client = Client(api_key, secret_key)
            request.session['client'] = client
            phone = request.user.phone
            print(f'{phone}')
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            message = f"Dear Prime User,\n Your Bot Verification Code is : {otp}. if this was not you, please inform support or info@gflightmode.com. Please do not share this OTP\nRegards GFM TeamOTP"
            send_otp(phone, message)
        except:
            return JsonResponse({"success": False, "message": f"Invalid secret key or api key{phone}"})

        return JsonResponse({"success": True, "message": "Otp has been sent"})

    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def start_bot(request):
        user_otp = request.GET['otp']
        otp = request.session.get('otp')
        if int(user_otp) != otp:
            return JsonResponse({"success": False, "message": "Phone Otp Not Verified"})
        request.session.delete('otp')
        sell_limit, buy_limit = 0.055, 0.045
        client = request.session.get('client')

        def on_open(ws):
            print("Started")

        def on_close(ws):
            # return JsonResponse({"msg": "Connection Closes"})
            print("Closed")

        def on_error(ws, error):
            print("error")
            return JsonResponse({"msg": f"{error}"})

        def order(side, quantity, symbol="FORUSDT"):
            try:
                order_ = client.create_order(symbol=symbol, side=side, type=client.ORDER_TYPE_MARKET, quantity=quantity)
                print(order_)
            except BinanceAPIException as ex:
                print(f"{ex}")
                return JsonResponse({"Failure": f"{ex}"})
            print("oderrrr placed")
            return JsonResponse({"msg": f"{order_}"})

        def on_message(ws, message, sell_limit=sell_limit, buy_limit=buy_limit):
            candle_data = json.loads(message)
            closing_rate = float(candle_data['k']['c'])
            if closing_rate >= sell_limit:
                order("SELL", 100)
            elif closing_rate <= buy_limit:
                order("BUY", 100)

        SYMBOL = 'forusdt'

        SOCKET = "wss://stream.binance.com:9443/ws/" + SYMBOL + "@kline_1m"
        websocket_app = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_error=on_error,
                                               on_message=on_message)
        websocket_app.run_forever()

    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def live_price(request):
        key = "https://api.binance.com/api/v3/ticker/price?symbol="
        currencies = ["BTCUSDT", "ETHUSDT", "AAVEUSDT"]
        data_list = []
        for i in currencies:
            url = key + i
            data = requests.get(url)
            data = data.json()
            data_list.append(data)
            # sock = f"wss://stream.binance.com:9443/ws/{i.lower()}@kline_1m"
        return JsonResponse({"data": data_list})
