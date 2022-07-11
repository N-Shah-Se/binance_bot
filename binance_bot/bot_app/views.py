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
from binance import BinanceSocketManager


sell_limit, buy_limit = 0, 0
client = None
from rest_framework.views import APIView
from user_account.views import send_otp
import random
from manual_trading.models import BotUser
from binance.enums import *
from rest_framework.response import Response
import os
import subprocess
from bot_app.models import Order
# Create your views here.
class price_info:
    bid_price = 0
    buy_counter = 0
    bot_started = True

class BotOperation(APIView):
    @api_view(['POST'])
    # @permission_classes([permissions.AllowAny])
    def check_credentials(request):
        authenticated = request.session.get('authenticated')
        if authenticated==False:
            return JsonResponse({"status": False, "message": "Please Login To Use The App"})
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
        if response_ ==False:
            return JsonResponse({"success": False, "message": "Invalid APi KEY and Secret Key"})
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
            'secret_key': secret_key,
            'otp':otp
        }
        return JsonResponse({"success": True, "message": "The OTP has been sent to your registered mobile number.","data":data})

    @api_view(['POST'])
    # @permission_classes([permissions.AllowAny])
    def start_bot(request):
        authenticated = request.session.get('authenticated')
        if authenticated==False:
            return JsonResponse({"status": False, "message": "Please Login To Use The App"})
        class test_class:
            client=''
            bidding=''
            tradeA = False
            tradeB = False
            user = ""
        user_otp = request.data['otp']
        otp = request.session.get('verification_otp')

        if int(user_otp) != otp:
            return JsonResponse({"status": False, "message": "Entered Otp is invalid"})
        user = request.user.email
        query_chk = BotUser.objects.filter(user=user)
        api_key = request.session.get('api_key')
        secret_key = request.session.get('secret_key')
        # api_key = request.data['api_key']
        # secret_key = request.data['secret_key']
        if not query_chk:
            BotUser.objects.create(user=request.user.email, api_key=api_key, secret_key=secret_key)
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
        # sell_limit, buy_limit = "", ""
        client = Client(api_key,secret_key)
        test_class.client=client
        # client = request.session.get('client')
        def place_order(side, quantity,price, symbol,profit='0'):
            try:
                order = test_class.client.create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=str(price)
                )
                print(order)
                order['email'] = request.user.email
            except BinanceAPIException as ex:
                print(f"{ex}")
            # Order.objects.create(order)
            if side==SIDE_SELL:
                order['profit'] = profit
            order_data = Order(**order)
            order_data.save()
            return order
            #
        while price_info.bot_started:
            symbol="XRPUSDT"
            try:
                current_price = float(test_class.client.get_symbol_ticker(symbol=symbol)["price"])
                current_price =float('{:.8f}'.format(current_price))
                print(current_price)
                if test_class.bidding == '':
                    test_class.bidding = current_price
                    order = place_order(SIDE_BUY,30,current_price,symbol)
                    print(current_price)
                    print(f"Buy Order : {order}")
                else:
                    previous_price = test_class.bidding
                    per1 = float(previous_price)/100 # 0.5 percent profit
                    per10 = (float(previous_price)*10)/100
                    per1 = float('{:.8f}'.format(per1))
                    per10 = float('{:.8f}'.format(per10))
                    per1_profit = float(previous_price) + per1
                    per1_profit = float('{:.8f}'.format(per1_profit))
                    per1_loss = float(previous_price) - per1
                    per1_loss = float('{:.8f}'.format(per1_loss))
                    per10_loss = float(previous_price) - per10
                    per10_loss = float('{:.8f}'.format(per10_loss))
                    print("Bidding Price : ",previous_price)
                    print("One Perc : ",per1 )
                    print("Ten Perc : ", per10)
                    print("Per1 Profit : ",per1_profit,"Per1 Loss : ",per1_loss,"Per10 Loss : ",per10_loss)
                    if float(current_price) >= per1_profit and test_class.tradeA==False :
                        print("***sell***")
                        print(current_price)
                        test_class.tradeA=True
                        test_class.bidding = current_price
                        order = place_order(SIDE_SELL, 29, current_price, symbol,per1)
                        print(f"{order}:::current_price{current_price}")
                    elif current_price <= per1_loss and test_class.tradeB==False:
                        print("buy")
                        print(current_price)
                        test_class.tradeB = True
                        test_class.tradeA=False
                        test_class.bidding = current_price
                        order = place_order(SIDE_BUY, 30, current_price, symbol)
                #         order(SIDE_BUY,10,current_price,symbol)
                #         buy_counter+=1
                #         print(f"BidPrice{bid_price}:::current_price{current_price}")
                    elif current_price < per10_loss  and test_class.tradeB:

                        order_sell = place_order(SIDE_SELL, 29, current_price, symbol)
                        sleep(30*60)
                        current_price = float(test_class.client.get_symbol_ticker(symbol=symbol)["price"])
                        current_price =float('{:.8f}'.format(current_price))
                        order_buy = place_order(SIDE_BUY, 30, current_price, symbol)

                        print(f"Order Sell : {order_sell}, Order Buy : {order_buy}")
                        test_class.bidding = current_price
                        print(current_price)
                        test_class.tradeB = False

            except Exception as ex:
                print(f"{ex}")
            sleep(3)
        return JsonResponse({"process":"Stoped"})



    # @api_view(['GET'])
    # # @permission_classes([permissions.AllowAny])
    # def start_bot(request):
    #     class test_class:
    #         client=''
    #         bidding=''
    #         buy_counter = 0
    #         user = ""
    #     user_otp = request.GET['otp']
    #     otp = request.session.get('verification_otp')

    #     if int(user_otp) != otp:
    #         return JsonResponse({"status": False, "message": "Entered Otp is invalid"})
    #     user = request.user.email
    #     query_chk = BotUser.objects.filter(user=user)
    #     api_key = request.session.get('api_key')
    #     secret_key = request.session.get('secret_key')
    #     # api_key = request.data['api_key']
    #     # secret_key = request.data['secret_key']
    #     if not query_chk:
    #         BotUser.objects.create(user=request.user.email, api_key=api_key, secret_key=secret_key)
    #     else:
    #         if query_chk:
    #             query_chk = BotUser.objects.get(user=user)
    #             data = {
    #                 'email': request.user.email,
    #                 'phone': request.user.phone,
    #                 'api_key': query_chk.api_key,
    #                 'secret_key': query_chk.secret_key
    #             }
    #             return JsonResponse({"success":True,"data":data})
    #     request.session.delete('verification_otp')
    #     request.session.delete('api_key')
    #     request.session.delete('secret_key')
    #     # sell_limit, buy_limit = "", ""
    #     client = Client(api_key,secret_key)
    #     test_class.client=client
    #     # client = request.session.get('client')


    #     def on_open(ws):
    #         print("Started")

    #     def on_close(ws):
    #         # return JsonResponse({"msg": "Connection Closes"})
    #         print("Closed")

    #     def on_error(ws, error):
    #         print("error")
    #         return JsonResponse({"msg": f"{error}"})

    #     def place_order(side, quantity,price, symbol):
    #         try:
    #             # order_ = client.create_order(symbol=symbol, side=side, type=client.ORDER_TYPE_MARKET, quantity=quantity)
    #             # quantity=
    #             # price=0.1000
    #             # client = request.session.get('client')
    #             # quantity=100
    #             # price=0.100
    #             # order = test_class.client.create_order(
    #             order = test_class.client.create_test_order(
    #             symbol=symbol,
    #             side=side,
    #             type=ORDER_TYPE_LIMIT,
    #             timeInForce=TIME_IN_FORCE_GTC,
    #             quantity=quantity,
    #             price=str(price)
    #             )
    #             print(order)
    #             # request.session['buy_limit'] = buy_limit
    #         except BinanceAPIException as ex:
    #             print(f"{ex}")
    #             # return JsonResponse({"Failure": f"{ex}"})
    #         print("oderrrr placed")
    #         # return JsonResponse({"msg": f"{order}"})
    #     def cancel_order():
    #         # client = request.session.get('client')
    #         # buy_limit = request.session.get('buy_limit')
    #         order_cancel = client.cancel_order(symbol=currency,orderId=buy_limit['orderId'])
    #         print(order_cancel)

    #     def on_message(ws,message, sell_limit=sell_limit, buy_limit=buy_limit):
    #         symbol="XRPUSDT"
    #         current_price = float(test_class.client.get_symbol_ticker(symbol=symbol)["price"])
    #         current_price =float('{:.8f}'.format(current_price))
    #         if test_class.bidding == '':
    #             test_class.bidding = current_price
    #             order = place_order(SIDE_BUY,30,current_price,symbol)
    #             # print(order)
    #             test_class.buy_counter+=1
    #             print(test_class.buy_counter)
    #             # print(order)
    #             # ws.close()
    #         else:
    #             previous_price = test_class.bidding
    #             per1 = (float(previous_price)*1)/100
    #             per1 = float('{:.8f}'.format(per1))
    #             per5 = (float(previous_price)*5)/100
    #             per5 = float('{:.8f}'.format(per5))
    #             per1_profit = float(previous_price) + per1
    #             per1_loss = float(previous_price) - per1
    #             per5_loss = float(previous_price) - per5
    #             if current_price >= per1_profit and test_class.buy_counter <= 2:
    #                 print("sell")
    #                 # test_class.buy_counter+=1
    #                 order = place_order(SIDE_SELL, 29, current_price, symbol)
    #                 # order(SIDE_SELL,10,current_price,symbol)
    #         #         print(f"BidPrice{bid_price}:::current_price{current_price}")
    #             elif current_price < per1_loss and test_class.buy_counter <= 3:
    #                 print("buy")
    #                 test_class.buy_counter+=1
    #                 order = place_order(SIDE_BUY, 30, current_price, symbol)
    #         #         order(SIDE_BUY,10,current_price,symbol)
    #         #         buy_counter+=1
    #         #         print(f"BidPrice{bid_price}:::current_price{current_price}")
    #             elif current_price < per5_loss and test_class.buy_counter <= 3:
    #                 print("buy")
    #                 test_class.buy_counter += 1
    #                 order = place_order(SIDE_BUY, 30, current_price, symbol)
    #             # elif test_class.buy_counter ==2:
    #             #     print("Bot Stooped")
    #             #     ws.close()

    #         #         order(SIDE_BUY,10,current_price,symbol)
    #         #         buy_counter+=1
    #         #         print(f"BidPrice{bid_price}:::current_price{current_price}")
    #         #     else:
    #         #         print(f"BidPrice{bid_price}:::current_price{current_price}")


    #         # price1 = msg['p']
    #         # if price1 > (float(price)*1)*100:
    #             # pass
    #         # sleep(30)
    #         # cancel_order(symbol)
    #         # if closing_rate >= sell_limit:
    #         #     order("SELL", 100)
    #         # elif closing_rate <= buy_limit:
    #         #     order("BUY", 100)
    #     SYMBOL = 'xrpusdt'
    #     SOCKET = "wss://stream.binance.com:9443/ws/" + SYMBOL + "@kline_1m"
    #     websocket_app = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_error=on_error,
    #                                           on_message=on_message)

    #     # request.session['websocket_app'] = websocket_app
    #     websocket_app.run_forever()
    #     return JsonResponse({"process":"Bot Stoped"})

    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def live_price(request):
        authenticated = request.session.get('authenticated')
        if authenticated==False:
            return JsonResponse({"status": False, "message": "Please Login To Use The App"})
        key = "https://api.binance.com/api/v3/ticker/price?symbol="
        currencies = ["BTCUSDT", "ETHUSDT", "AAVEUSDT","XRPUSDT"]
        data_list = []
        for i in currencies:
            url = key + i
            data = requests.get(url)
            data = data.json()
            data_list.append(data)
            # sock = f"wss://stream.binance.com:9443/ws/{i.lower()}@kline_1m"
        return JsonResponse({"data": data_list})


    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def stop_bot(request):
        authenticated = request.session.get('authenticated')
        if authenticated==False:
            return JsonResponse({"status": False, "message": "Please Login To Use The App"})

        if price_info.bot_started:
            price_info.bot_started = False
        else:
            return JsonResponse({"status": False, "message": "Bot is Already Stoped."})
        # key = "https://api.binance.com/api/v3/ticker/price?symbol="
        # currencies = ["BTCUSDT", "ETHUSDT", "AAVEUSDT","XRPUSDT"]
        # data_list = []
        # for i in currencies:
        #     url = key + i
        #     data = requests.get(url)
        #     data = data.json()
        #     data_list.append(data)
            # sock = f"wss://stream.binance.com:9443/ws/{i.lower()}@kline_1m"
        return JsonResponse({"status": True, "message": "Bot is stoped Successfully."})


    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def trade_profit(request):
        authenticated = request.session.get('authenticated')
        if authenticated==False:
            return JsonResponse({"status": False, "message": "Please Login To Use The App"})
        order_data =Order.objects.filter(side="SELL").filter(email=request.user.email)
        total_data = []

        sum = 0.0
        if order_data:
            for prof in order_data:
                user_profit_data = {}
                user_profit_data['transactTime'] = prof.transactTime
                user_profit = float(prof.profit)
                user_profit_data['user_profit'] = user_profit
                sum += user_profit
                total_data.append(user_profit_data)
        data = {"sum":sum,'individual':total_data}

        return JsonResponse({"data": data })



