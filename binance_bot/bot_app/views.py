from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
import websocket, json
from binance.exceptions import BinanceAPIException
from binance.client import Client
from rest_framework import response, permissions
from rest_framework.decorators import permission_classes
sell_limit,buy_limit = 0,0
client = None
from rest_framework.views import APIView

class BotOperation(APIView):
    @api_view(['POST'])
    @permission_classes([permissions.AllowAny])
    def start_bot(request):
        api_key = request.data['api_key']
        secret_key = request.data['secret_key']
        try:
            client = Client(api_key, secret_key)
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