from django.urls import path, include
from .views import discount,referal_code
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
    path('referal_code/',referal_code.get_referal_code, name="referal_code")
    # path('verify/', verify_jwt_token, name='verify_token'),
]
