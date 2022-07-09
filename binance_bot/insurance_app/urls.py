from django.urls import path, include
from .views import KycUser
# from rest_framework_jwt.views import  (
#     obtain_jwt_token,
#     refresh_jwt_token,
#     verify_jwt_token,
# )

urlpatterns = [
    path('add_insurance/',KycUser.add_data),
    # path('get_status/',KycUser.get_status),
]
