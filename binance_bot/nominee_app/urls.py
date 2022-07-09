from django.urls import path, include
from .views import Nominee
# from rest_framework_jwt.views import  (
#     obtain_jwt_token,
#     refresh_jwt_token,
#     verify_jwt_token,
# )

urlpatterns = [
    path('add_nominee/',Nominee.add_data),
    path('get_status/',Nominee.get_status),
]
