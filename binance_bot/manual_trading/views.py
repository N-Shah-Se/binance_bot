from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
import websocket, json
from binance.exceptions import BinanceAPIException
from binance.client import Client
from rest_framework import response, permissions
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from manual_trading.models import BotUser
sell_limit,buy_limit = 0,0
client = None

from django.contrib.auth.decorators import login_required


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
		# import pdb; pdb.set_trace()
		bot_users = BotUser.objects.all()
		# HttpResponse('hello msg')
		return render(request, 'manual_trading.html', {"bot_users":bot_users})

def start_manual(request):
	# import pdb; pdb.set_trace()
	# email = request.get()
	return HttpResponse('Hello')