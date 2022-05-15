from django.urls import path, include
from .views import UserRegisteration

urlpatterns = [
    # path('verify/<int:phone>',getPhoneNumberRegistered),
    path('get_phone_otp/<str:phone>',UserRegisteration.get_phone_otp),
    path('verify_phone/',UserRegisteration.phone_verfication),
    path('get_email_otp/<str:email>',UserRegisteration.get_email_otp),
    path('verify_email/',UserRegisteration.email_verification),
    path('add_user/',UserRegisteration.add_user),
    path('login_user/',UserRegisteration.userLogin),
    path('change_password/',UserRegisteration.change_password),
]
