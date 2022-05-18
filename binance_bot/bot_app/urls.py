from django.urls import path, include
from .views import *

urlpatterns = [
    # path('verify/<int:phone>',getPhoneNumberRegistered),
    path('start_bot/',start_bot),
]
