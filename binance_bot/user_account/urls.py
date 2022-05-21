from django.urls import path, include
from .views import UserRegisteration, OtpOperation

urlpatterns = [
    # path('verify/<int:phone>',getPhoneNumberRegistered),
    path('get_phone_otp/<str:phone>',OtpOperation.get_phone_otp),
    path('verify_phone/',OtpOperation.phone_verfication),
    path('get_email_otp/<str:email>',OtpOperation.get_email_otp),
    path('verify_email/',OtpOperation.email_verification),
    path('add_user/',OtpOperation.add_user),
    path('login_user/',UserRegisteration.userLogin),
    path('change_password/',UserRegisteration.change_password),
]
