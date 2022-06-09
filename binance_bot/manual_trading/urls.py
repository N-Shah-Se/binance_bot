from django.urls import path
from . import views
urlpatterns = [
    path('get_credentials/',views.ManualOperation.get_credentials),
    path('place_order/',views.ManualOperation.place_order),
    path('cancel_order/',views.ManualOperation.cancel_order),
    path('get_currency_data/',views.ManualOperation.get_currency_data),
    # path('cancel_order/',views.ManualOperation.cancel_order),

]