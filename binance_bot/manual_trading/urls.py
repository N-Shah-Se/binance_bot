from django.urls import path
from .views import *
from .import views

urlpatterns = [
    # path('verify/<int:phone>',getPhoneNumberRegistered),
    # path('check_credentials/',ManualOperation.check_credentials),
    # path('start_manual/',ManualOperation.start_bot),
    path('get_credentials/',ManualOperation.get_credentials),
    # path('bot_users_list/',ManualOperation.manual_trading),
    # path('bot_users_list/manual/', ManualOperation.start_manual),
    # path('', views.start_manual, name='start_manual'),
]