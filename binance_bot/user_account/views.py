import re
from django.shortcuts import render, redirect
from .models import Profile
import requests
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from .serializer import UserSerializer
from rest_framework import views, status
from user_account.permissions import AllowOptionsAuthentication
from rest_framework import response, permissions


# Create your views here.


def send_otp(number, message):
    url = "https://www.fast2sms.com/dev/bulk"
    api = "pnUzB8jDOqNR3tVcLAFx02ifvCKJdlwu5oQyTMPXr79mbS6eZ1B5XrIh61zdGHA89u3aw4FCJtYnpbQe"
    querystring = {"sender_id": "FSTSMS", "message": message, "language": "english", "route": "p",
                   "numbers": number}
    headers = {
        'authorization': api,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }
    return requests.request("POST", url, data=querystring, headers=headers)


class OtpOperation(views.APIView):
    permission_classes = [permissions.AllowAny]

    @api_view(['GET'])
    def get_phone_otp(request):
        phone = request.GET['phone']
        call_for = request.GET['call_for']
        request.session['phone'] = phone
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        if call_for.lower() == 'signup':
            message = f"Dear Prime User,\nYour Signup OTP for  G Flight MODE is {otp}. if this was not you, please inform support or info@gflightmode.com. Please do not share this OTP\nRegards GFM TeamOTP"
        if call_for.lower() == 'login':
            message = f"Dear Prime User,\n Your Login OTP for  G Flight MODE is {otp}. if this was not you, please inform support or info@gflightmode.com. Please do not share this OTP\nRegards GFM TeamOTP"
        if call_for.lower() == 'forgot_password':
            message = f"Dear Prime User,\n Your OTP for forgot password to G Flight MODE is {otp}. if this was not you, please inform support or info@gflightmode.com. Please do not share this OTP\nRegards GFM TeamOTP"
        a = send_otp(phone, message)
        if a:
            return JsonResponse({"msg": 'OTP send Successfully'})
        else:
            return JsonResponse({"msg": "OTP is sent your phone "})

    @api_view(['GET'])
    def phone_verfication(request):
        user_otp = request.GET['otp']
        otp = request.session.get('otp')

        if int(user_otp) == otp:
            request.session.delete('otp')
            return JsonResponse({"msg": "Verified"})
        else:
            return JsonResponse({"msg": "Wrong OTP"})

    @api_view(['GET'])
    def get_email_otp(request):
        otp = random.randint(100000, 999999)
        request.session['email_otp'] = otp
        email = request.GET['email']
        call_for = request.GET['call_for']
        request.session['email'] = email
        message = ""
        if call_for.lower() == 'signup':
            message = f"Dear Prime User,\nYour Signup OTP for  G Flight MODE is {otp}. if this was not you, please inform support or info@gflightmode.com. Please do not share this OTP\nRegards GFM TeamOTP"
        if call_for.lower() == 'login':
            message = f"Dear Prime User,\nYour Login OTP for  G Flight MODE is {otp}. if this was not you, please inform support or info@gflightmode.com. Please do not share this OTP\nRegards GFM TeamOTP"
        if call_for.lower() == 'forgot_password':
            message = f"Dear Prime User,\n Your OTP for forgot password to G Flight MODE is {otp}. if this was not you, please inform support or info@gflightmode.com. Please do not share this OTP\nRegards GFM TeamOTP"
        send_mail(
            'Email Verification OTP',
            message,
            'settings.EMAIL_HOST_USER',
            [email],
            fail_silently=False, )
        return JsonResponse({"msg": "OTP send to your email successfully"})

    @api_view(["POST"])
    def email_verification(request):
        user_otp = request.GET['otp']
        otp = request.session.get('email_otp')
        if int(user_otp) == otp:
            request.session.delete('email_otp')
            return JsonResponse({"msg": "Email Verified"})
        else:
            return JsonResponse({"msg": "Email Not Verified"})

    @api_view(['POST'])
    def add_user(request):
        password = request.GET['password']
        phone_otp = request.GET['phone_otp']
        email_otp = request.GET['email_otp']
        invitation_code = request.GET['invitation_code']
        # email = request.session.get('email_otp')
        # phone = request.session.get('otp')
        # #        otp = request.session['email_otp']
        # if int(email_otp) == email and int(phone_otp) == phone:
        #     pass
        # elif int(email_otp) != email:
        #     return JsonResponse({"msg": f"Email Not Verified{email}{email_otp}"})
        # elif int(phone_otp) != phone:
        #     return JsonResponse({"msg": f"Wrong OTP{phone}{phone_otp}"})

        # email = request.session.get('email')
        # phone = request.session.get('phone')

        # hash_pwd = make_password(password)
        emails = Profile.objects.filter(email=email_otp)
        phone_no = Profile.objects.filter(phone=phone_otp)
        account_exist = False
        if emails:
            account_exist = True
        if phone_no:
            account_exist = True

        if account_exist:
            return JsonResponse({"msg": "Account already exist"})
        else:
            request.data._mutable = True
            password = request.data['password']
            request.data['password'] = make_password(password)
            request.data._mutable = False
            Users = UserSerializer(data=request.data)

            if Users.is_valid():
                Users.save()
            if status.HTTP_200_OK:
                return JsonResponse({"User Id": Users.data['id']})
            elif status.HTTP_500_INTERNAL_SERVER_ERROR:
                return JsonResponse({"error": "Internal Server Error"})
            # Profile.objects.create_user(
            #     email=email,
            #     phone=phone,
            #     invitation_code=invitation_code,
            #     password=password
            # )
            request.session.delete('email_otp')
            request.session.delete('phone_otp')
            return JsonResponse({"msg": "User Account created"})


class UserRegisteration(APIView):
    permission_classes = (AllowOptionsAuthentication,)

    @api_view(['GET'])
    def userLogin(request):
        password = request.GET['password']
        operation = request.GET['operation']
        otp = request.GET['otp']
        if '@' in str(operation):
            email = request.session.get('email_otp')
            if int(otp) != email:
                return JsonResponse({"msg": f"Email Not Verified{email}{otp}"})
            user = Profile.objects.filter(email=operation)
        else:
            phone = request.session.get('otp')
            if int(otp) != phone:
                return JsonResponse({"msg": f"Wrong OTP{phone}{otp}"})
            user = Profile.objects.filter(phone=operation)
        user_password = ""
        for ps in user:
            user_password = ps.password
        #print(f"{user}")
        if check_password(password,user_password):
            #if #check_password(password, user_password):
            return JsonResponse({"msg": "Login Successfully"})
            #else:
             #   return JsonResponse({"msg": f"Password Not Matched {user_password}"})
        else:
            return JsonResponse({"msg": f"Login Failed {user}"})

    @api_view(['POST'])
    def change_password(request):
        password = request.GET['password']
        email = request.session.get('email')
        phone = request.session.get('phone')
        user = Profile.objects.filter(email=email).filter(phone=phone)
        user.update(password=make_password(password))
        return JsonResponse({"msg": "Password Changed"})
