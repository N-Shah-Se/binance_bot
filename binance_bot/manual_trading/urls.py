from django.urls import path
from .views import *
from .import views

urlpatterns = [
    path('get_credentials/',ManualOperation.get_credentials),

]