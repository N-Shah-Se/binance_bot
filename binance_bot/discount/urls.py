from unicodedata import name
from django.urls import path, include
from .views import discount,referal_code,leadership_bonus, re_top_up_bonus
# from .views import UserRegisteration, OtpOperation
# from .views import OtpOperation
# from rest_framework_jwt.views import  (
#     obtain_jwt_token,
#     refresh_jwt_token,
#     verify_jwt_token,
# )

urlpatterns = [
    path('discount_bonus/', discount.discount_bonus, name='discount bonus'),
    path('direct_bonus/', discount.direct_bonus, name='direct_bonus'),
    path('referal_code/',referal_code.get_referal_code, name="referal_code"),
    path('leadership_bonus/',leadership_bonus.as_view(), name="leadership_bonus"),
    path('bonus/', discount.user_bonus, name='user_bonus' ),
    path('retopup/', re_top_up_bonus.as_view(), name="re_top_up_bonus" )
    # path('verify/', verify_jwt_token, name='verify_token'),
]
