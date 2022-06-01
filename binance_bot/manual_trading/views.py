from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
import websocket, json
from binance.exceptions import BinanceAPIException
# from binance.client import Client
from django.views.generic import (
	TemplateView
)
from rest_framework import response, permissions
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from manual_trading.models import BotUser
sell_limit,buy_limit = 0,0
client = None

from django.contrib.auth.decorators import login_required
import requests

class ManualOperation(APIView):
	@api_view(['POST'])
	@permission_classes([permissions.AllowAny])
	def start_bot(request):
		import pdb;
		pdb.set_trace()
		print(request.user.id)
		api_key = request.data['api_key']
		secret_key = request.data['secret_key']
		user_id = request.user.id
		try:
			client = Client(api_key, secret_key)
			if client:
				query_chk = BotUser.objects.filter(user__id=user_id)
				if not query_chk:
					BotUser.objects.create(user = user_id, api_key=api_key, secret_key=secret_key, email=email)

		except:
			return JsonResponse({"success":False,"message":"Wrong API key"})
		request.session['client'] = client
		sell_limit, buy_limit = 0.055, 0.045

		# return JsonResponse({"a":"b"})
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
			except BinanceAPIException as ex:
				return JsonResponse({"Failure": f"{ex}"})
			return JsonResponse({"msg": f"{order_}"})

		def on_message(ws, message, sell_limit=sell_limit, buy_limit=buy_limit):
			candle_data = json.loads(message)
			closing_rate = float(candle_data['k']['c'])
			if closing_rate >= sell_limit:
				order("SELL", 100)
			elif closing_rate <= buy_limit:
				order("BUY", 100)

		websocket_app = websocket.WebSocketApp(settings.SOCKET, on_open=on_open, on_close=on_close, on_error=on_error,
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
			# data = data.json()
			data_list.append(data)
		return JsonResponse({"data": data_list})


	@permission_classes([permissions.AllowAny])
	@login_required
	def manual_trading(request):
		bot_users = BotUser.objects.all()
		# HttpResponse('hello msg')
		return render(request, 'manual_trading.html', {"bot_users":bot_users})


def start_manual(request):
	from django.urls import reverse
	query_dict = request.GET
	email = query_dict.get('email_id')
	print(email)
	act_user = BotUser.objects.filter(user__email=email)
	if act_user:
		email_obj = email
		#return render(request, 'manual_trading_buy_sell.html', {})
		return JsonResponse({
			'url': reverse('ManualTradingBuySellTemplateView'),'email':str(email)
		})

class ManualTradingBuySellTemplateView(TemplateView):
	template_name = "manual_trading_buy_sell.html"
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		# context['email'] = 'ranjeetcoding@gmail.com'
		# email = 'admin@gmail.com'
		email = 'nasirshahrst@gmail.com'
		# print(context)
		from binance.spot import Spot as Client
		bot_obj = BotUser.objects.filter(user__email=email)
		# print(context['botuser'][0].api_key)
		api_key = bot_obj[0].api_key
		secret_key = bot_obj[0].secret_key
		base_url = 'https://api.binance.com'
		client = Client(api_key, secret_key)


		## end account api call##


		api_trade = 'https://api.binance.com/api/v1/ticker/allPrices'
		data = requests.get(api_trade)
		context['data'] = data

		print(context.get('data'))
		response_txt = json.loads(context.get('data').text)
		context['data'] = response_txt
		# return JsonResponse({"data": data})


		# import requests, hashlib, hmac
		# from urllib.parse import urlencode

		# account = client.account()
		# account_obj = json.loads(account.text)
		# mytrades = client.my_trades('BTCUSDT')
		# timestamp = 'https://api.binance.com/api/v3/time'
		# servertime  = requests.get(timestamp)
		# servertimeobject = json.loads(servertime.text)
		# timestamp = servertimeobject['serverTime']
		# print(timestamp)

		# userdata = requests.get("https://api.binance.com/api/v3/myTrades",
		#     params = urlencode({
		#     	"symbol" : "BTCUSDT",
		#         "signature" : hmac.new(secret_key.encode()),
		#         "timestamp" : timestamp,
		#     }),
		#     headers = {
		#         "X-MBX-APIKEY" : api_key,
		#     }
		# )
		# print(userdata.text)

		return context


