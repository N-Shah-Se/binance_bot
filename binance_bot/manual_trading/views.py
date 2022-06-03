from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
import websocket, json
from binance.exceptions import BinanceAPIException
from binance.client import Client
from django.views.generic import (
	TemplateView
)
from rest_framework import response, permissions
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from manual_trading.models import BotUser
from django.contrib.auth.decorators import login_required
class ManualOperation(APIView):

	@api_view(['GET'])
	@permission_classes([permissions.AllowAny])
	def get_credentials(request):
		try:
			query_chk = BotUser.objects.get(user=request.user)
		except:
			return JsonResponse({"success": False, "message": "User API key and Secret Key is not availabel"})

		data = {
			'api_key': query_chk.api_key,
			'secret_key': query_chk.secret_key
		}
		return JsonResponse({"data": data, "message": "User Data"})
