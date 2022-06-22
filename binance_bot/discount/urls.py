from django.urls import path, include
from .views import discount
# from .views import UserRegisteration, OtpOperation
# from .views import OtpOperation
# from rest_framework_jwt.views import  (
#     obtain_jwt_token,
#     refresh_jwt_token,
#     verify_jwt_token,
# )

urlpatterns = [
    path('discount_bonus/', discount.bonus_discount, name='discount bonus'),
    path('direct_discount/', discount.direct_discount, name='direct_discount'),
    # path('verify/', verify_jwt_token, name='verify_token'),
]
