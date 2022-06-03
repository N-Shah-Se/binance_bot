from django.urls import path
from . import views
urlpatterns = [
    path('get_credentials/',ManualOperation.get_credentials),

]