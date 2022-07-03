from django.urls import path
from . import views    

from django.contrib.auth import views as authViews

urlpatterns = [
    path('home/' ,views.home , name="home"),
    path('bot_users/' ,views.bot_users , name="bot_users"),
  # path('customer/' ,views.customer),
  #   path('customer/<str:pk>' ,views.customer, name="customer"),
  # #  path('create/' ,views.create, name="create"),
  #   path('create/<str:pk>' ,views.create, name="create"),
  #   path('update/<str:pk>' ,views.update, name="update"),
  #   path('delete/<str:pk>' ,views.delete, name="delete"),
  #   path('register/' ,views.register, name="register"),
    path('' ,views.userLogin, name="login"),
    path('forgot_password/' ,views.forgot_password, name="forgot_password"),
    path('logout/' ,views.userLogout, name="logout"),
    path('accounts/' ,views.accounts, name="accounts"),
    path('email_otp/' ,views.email_otp, name="email_otp"),
    path('change_password/' ,views.change_password, name="change_password"),
    # path('accounts/' ,views.accounts, name="accounts"),
    # path('profile/' ,views.profileInfo, name="profile_info"),




     # path('reset_password/' ,authViews.PasswordResetView.as_view(template_name= "bookstore/password_reset.html") , name="reset_password"),
     # path('reset_password_sent/' ,authViews.PasswordResetDoneView.as_view(template_name= "bookstore/password_reset_sent.html") , name="password_reset_done"),
     # path('reset/<uidb64>/<token>/' ,authViews.PasswordResetConfirmView.as_view(template_name= "bookstore/password_reset_form.html") , name="password_reset_confirm"),
     # path('reset_password_complete/' ,authViews.PasswordResetCompleteView.as_view(template_name= "bookstore/password_reset_done.html") , name="password_reset_complete"),

]