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
from manual_trading.models import BotUser


# Create your views here.

class BotOperation(APIView):
    @api_view(['POST'])
    @permission_classes([permissions.AllowAny])
    def check_credentials(request):
        api_key = request.data['api_key']
        secret_key = request.data['secret_key']
        try:
            url = 'https://api.binance.com/api/v1/userDataStream'
            response_ = requests.post(url, headers={'X-MBX-APIKEY': api_key})  # ['listenKey']
            if response_:
                client = Client(api_key, secret_key)
                request.session['client'] = client
                request.session['api_key'] = api_key
                request.session['secret_key'] = secret_key
            # user = request.user
            # query_chk = BotUser.objects.filter(user=user)
            # if not query_chk:
            #     bot_user = BotUser.objects.create(user=request.user,api_key=api_key,secret_key=secret_key)

        except:
            return JsonResponse({"success": False, "message": "Invalid secret key or api key"})

        phone = request.user.phone
        print(f'{phone}')
        otp = random.randint(100000, 999999)
        request.session['verification_otp'] = otp
        message = f"Dear Prime User,\n Your Bot Verification Code is : {otp}. if this was not you, please inform support or info@gflightmode.com. Please do not share this OTP\nRegards GFM TeamOTP"
        send_otp(phone, message)

        # if query_chk:
        #     query_chk = BotUser.objects.get(user=user)
        #     data = {
        #         'email': request.user.email,
        #         'phone': request.user.phone,
        #         'api_key': query_chk.api_key,
        #         'secret_key': query_chk.secret_key
        #     }
        #     return JsonResponse({"success":True,"data":data}
        data = {
            'email': request.user.email,
            'phone': request.user.phone,
            'api_key': api_key,
            'secret_key': secret_key
        }
        return JsonResponse({"success": True, "message": "The OTP has been sent to your registered mobile number.","data":data})

    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def start_bot(request):
        user_otp = request.GET['otp']
        otp = request.session.get('verification_otp')
        if int(user_otp) != otp:
            return JsonResponse({"success": False, "message": "Phone Otp Not Verified"})
        user = request.user
        query_chk = BotUser.objects.filter(user=user)
        api_key = request.session.get('api_key')
        secret_key = request.session.get('secret_key')
        if not query_chk:
            bot_user = BotUser.objects.create(user=request.user, api_key=api_key, secret_key=secret_key)
        else:
            if query_chk:
                query_chk = BotUser.objects.get(user=user)
                data = {
                    'email': request.user.email,
                    'phone': request.user.phone,
                    'api_key': query_chk.api_key,
                    'secret_key': query_chk.secret_key
                }
                return JsonResponse({"success":True,"data":data})
        request.session.delete('verification_otp')
        request.session.delete('api_key')
        request.session.delete('secret_key')
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
            print(message)
            closing_rate = float(candle_data['k']['c'])
            if closing_rate >= sell_limit:
                order("SELL", 100)
            elif closing_rate <= buy_limit:
                order("BUY", 100)
        SYMBOL = 'forusdt'
        SOCKET = "wss://stream.binance.com:9443/ws/" + SYMBOL + "@kline_1m"
        websocket_app = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_error=on_error,
                                               on_message=on_message)

        request.session['websocket_app'] = websocket_app
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
