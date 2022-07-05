from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
import websocket, json
from binance.exceptions import BinanceAPIException,BinanceOrderException,BinanceRequestException,BinanceOrderMinAmountException,BinanceOrderMinPriceException,BinanceOrderMinTotalException,BinanceOrderUnknownSymbolException,BinanceOrderInactiveSymbolException
from binance.client import Client
from django.views.generic import (
	TemplateView
)
from time import sleep
from rest_framework import response, permissions
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from manual_trading.models import BotUser
from binance.enums import *
from bot_app.models import Order

class ManualOperation(APIView):
	@api_view(['GET'])
	@permission_classes([permissions.AllowAny])
	def get_credentials(request):
		try:
		    authenticated = request.session.get('authenticated')
		    if authenticated==False:
		        return JsonResponse({"status": False, "message": "Please Login To Use The App"})
		    query_chk = BotUser.objects.get(user=request.user.email)
		except:
			return JsonResponse({"success": False, "message": "User API key and Secret Key is not availabel"})

		data = {
			'api_key': query_chk.api_key,
			'secret_key': query_chk.secret_key
		}
		return JsonResponse({"data": data, "message": "User Data"})

	@api_view(['GET'])
	@permission_classes([permissions.AllowAny])
	def place_order(request):
	    authenticated = request.session.get('authenticated')
	    if authenticated==False:
	        return JsonResponse({"status": False, "message": "Please Login To Use The App"})
	    api_key = request.data['api_key']
	    secret_key = request.data['secret_key']
	    currency = request.data['currency']
	   # minQty = request.GET['minQty']
	   # maxQty = request.GET['maxQty']
	    operation = request.data['operation']
	    if operation.lower() == "buy":
	        side=SIDE_BUY
	    else:
	        side = SIDE_SELL
	   # price = request.GET['price']
	   # quantity = request.GET['quantity']
	   # quantity=100
	   # price=0.1000

	    try:

	        client = Client(api_key, secret_key)
	        current_price = float(client.get_symbol_ticker(symbol=currency)["price"])
	        current_price =float('{:.8f}'.format(current_price))
	        request.session['client'] = client
	        place_order = client.create_order(
            symbol=currency,
            side=side,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity)

	   # try:
	   #     if operation == 'BUY':
	   #         info = client.futures_exchange_info() # request info on all futures symbols
	   #         symbols_n_precision = {}
	   #         for item in info['symbols']:
	   #             if item['symbol'] == currency:
	   #                 symbols_n_precision[item['symbol']] = item['quantityPrecision'] # not really necessary but here we are...
	   #         trade_size_in_dollars = quantity
	   #         # For example
	   #         order_amount = float(trade_size_in_dollars) / float(price) # size of order in BTC
	   #         precision = symbols_n_precision[currency]
	   #         precise_order_amount = "{:0.0{}f}".format(order_amount, precision)
	   #         buy_limit=client.create_order(symbol=currency, side='BUY', type='MARKET',timeInForce='GTC', quantity=quantity,price=price)
	   #        # buy_limit=client.futures_create_order(symbol=currency, side='BUY', type='MARKET', quantity=precise_order_amount)
	   #        # buy_limit = client.create_test_order(symbol=currency,side='SELL',type='LIMIT',quantity=100,timeInForce='GTC',price=price)
	       # elif operation == 'SELL':
	       #     buy_limit = client.create_order(symbol=currency,side='SELL',type='LIMIT',timeInForce='GTC',price=amount)
	    except BinanceAPIException as e:
	        return JsonResponse({"status":False,"message":f"{e}"})
	    except BinanceOrderException as e:
	        return JsonResponse({"status":False,"message":f"{e}"})
	    except BinanceRequestException as e:
	        return JsonResponse({"status":False,"message":f"{e}"})
	    except BinanceOrderMinAmountException as e:
	        return JsonResponse({"status":False,"message":f"{e}"})
	    except BinanceOrderMinPriceException as e:
	        return JsonResponse({"status":False,"message":f"{e}"})
	    except BinanceOrderMinTotalException as e:
	        return JsonResponse({"status":False,"message":f"{e}"})
	    except BinanceOrderUnknownSymbolException as e:
	        return JsonResponse({"status":False,"message":f"{e}"})
	    except BinanceOrderInactiveSymbolException as e:
	        return JsonResponse({"status":False,"message":f"{e}"})

	    request.session['buy_limit'] = place_order
	    Order.objects.create(place_order)
	    return JsonResponse({"status":True,"message":place_order})

	@api_view(['GET'])
	@permission_classes([permissions.AllowAny])
	def cancel_order(request):
	    authenticated = request.session.get('authenticated')
	    if authenticated==False:
	        return JsonResponse({"status": False, "message": "Please Login To Use The App"})
	    buy_limit = request.session.get('buy_limit')
	    currency = request.body['currency']
	    client = request.session.get('client')
	    cancel = client.cancel_order(symbol=currency,orderId=buy_limit['orderId'])
	    return JsonResponse({"status":True,"message":f"{cancel}"})

	@api_view(['GET'])
	@permission_classes([permissions.AllowAny])
	def get_currency_data(request):
	    authenticated = request.session.get('authenticated')
	    if authenticated==False:
	        return JsonResponse({"status": False, "message": "Please Login To Use The App"})
	   # buy_limit = request.session.get('buy_limit')
	    api_key = request.data['api_key']
	    secret_key = request.data['secret_key']
	    client = Client(api_key, secret_key)
	    currency_list = ['LTCUSDT','XRPUSDT','BNBUSDT','GALAUSDT','DOTUSDT','AAVEUSDT']
	    data = {}
	    for i in currency_list:
	        info = client.get_symbol_info(i)
	       # data.append({"maxQty":info['filters'][2]['maxQty']})
	       # sleep(2)
	        data[str(i)] = {}
	        data[i]['tickSize'] = info['filters'][0]['tickSize']
	        data[i]['maxQty'] = info['filters'][2]['maxQty']
	        data[i]['minQty'] = info['filters'][2]['minQty']
	        data[i]['minNotional'] = info['filters'][3]['minNotional']

	   # data['minQty']=info['filters'][2]['minQty']
	   # data['maxQty']=info['filters'][2]['maxQty']

	   # client = request.session.get('client')
	   # timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1m')
	   # bars = client.get_historical_klines('BTCUSDT', '1m', timestamp, limit=1000)
	   # cancel = client.cancel_order(symbol='ETHUSDT',orderId=buy_limit['orderId'])
	    return JsonResponse({"status":True,"data":data})
