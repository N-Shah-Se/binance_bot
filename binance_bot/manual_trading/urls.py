from django.urls import path
from . import views
urlpatterns = [
    path('get_credentials/',views.ManualOperation.get_credentials),

]