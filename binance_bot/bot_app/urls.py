from django.urls import path, include
from .views import *

urlpatterns = [
    # path('verify/<int:phone>',getPhoneNumberRegistered),
    path('check_credentials/',BotOperation.check_credentials),
    path('start_bot/',BotOperation.start_bot),
    path('live_price/',BotOperation.live_price),
    # path('profit_calculator/',BotOperation.profit_calculator),
]
