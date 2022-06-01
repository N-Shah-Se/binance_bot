from django.urls import path
from .views import *
from .import views

urlpatterns = [
    path('trading-sell-buy/', ManualTradingBuySellTemplateView.as_view(),
        name="ManualTradingBuySellTemplateView"),
    path('bot_users_list/',ManualOperation.manual_trading),
    path('', views.start_manual, name='start_manual'),
]