from django.urls import path
from .views import *
from .import views

urlpatterns = [
<<<<<<< HEAD
    # path('verify/<int:phone>',getPhoneNumberRegistered),
    # path('check_credentials/',ManualOperation.check_credentials),
    # path('start_manual/',ManualOperation.start_bot),
    path('get_credentials/',ManualOperation.get_credentials),
    # path('bot_users_list/',ManualOperation.manual_trading),
    # path('bot_users_list/manual/', ManualOperation.start_manual),
    # path('', views.start_manual, name='start_manual'),
=======
    path('trading-sell-buy/', ManualTradingBuySellTemplateView.as_view(),
        name="ManualTradingBuySellTemplateView"),
    path('bot_users_list/',ManualOperation.manual_trading),
    path('', views.start_manual, name='start_manual'),
>>>>>>> 54deb77b0c209e8d69ad2576f7468ab25114f57f
]