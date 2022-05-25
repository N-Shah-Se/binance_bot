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
from rest_framework import views, status, serializers
from rest_framework import response, permissions
from rest_framework.decorators import permission_classes
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


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

    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
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
            return JsonResponse({"success": True, "message": 'Phone OTP sent Successfully'})
        else:
            # return JsonResponse({"success": False, "message": 'OTP Sending Failed'})
            res = serializers.ValidationError({'message':'OTP Sending Failed', 'status_code':'400'})
            raise res


    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def phone_verfication(request):
        user_otp = request.GET['otp']
        otp = request.session.get('otp')

        if int(user_otp) == otp:
            request.session.delete('otp')
            return JsonResponse({"success": True, "message": "Phone Otp Verified"})
        else:
            # return JsonResponse({"success": False, "message": "Phone Otp Not Verified"})
            res = serializers.ValidationError({'message':'Phone Otp Not Verified', 'status_code':'400'})
            raise res

    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
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
        if status.HTTP_200_OK:
            return JsonResponse({"success": True, "message": 'OTP send Successfully'})
        else:
            # return JsonResponse({"success": False, "message": 'OTP Sending Failed'})
            res = serializers.ValidationError({'message':'OTP Sending Failed', 'status_code':'400'})
            raise res

    @api_view(["POST"])
    @permission_classes([permissions.AllowAny])
    def email_verification(request):
        user_otp = request.GET['otp']
        otp = request.session.get('email_otp')
        if int(user_otp) == otp:
            request.session.delete('email_otp')
            return JsonResponse({"success": True, "message": "Otp Verified"})
        else:
            # return JsonResponse({"success": False, "message": "Email Otp Not Verified"})
            res = serializers.ValidationError({'message':'Email OTP not verified', 'status_code':'400'})
            raise res


class UserRegisteration(APIView):
    # permission_classes = (AllowOptionsAuthentication,)
    # permission_classes = (permission_classes.IsAuthenticated,)
    @api_view(['POST'])
    @permission_classes([permissions.AllowAny])
    def add_user(request):
        password = request.GET['password']
        phone_otp = request.GET['phone_otp']
        email_otp = request.GET['email_otp']
        invitation_code = request.GET['invitation_code']
        email = request.session.get('email_otp')
        phone = request.session.get('otp')
        # #        otp = request.session['email_otp']
        if int(email_otp) == email and int(phone_otp) == phone:
            pass
        elif int(email_otp) != email:
            # return JsonResponse({"success": False, "message": "Email Otp Not Verified"})
            res = serializers.ValidationError({'message':'Email OTP not verified', 'status_code':'400'})
            raise res
        elif int(phone_otp) != phone:
            # return JsonResponse({"success": False, "message": "Phone Otp Not Verified"})
            res = serializers.ValidationError({'message':'Phone OTP not verified', 'status_code':'400'})
            raise res

        email = request.session.get('email')
        phone = request.session.get('phone')

        # hash_pwd = make_password(password)
        emails = Profile.objects.filter(email=email_otp)
        phone_no = Profile.objects.filter(phone=phone_otp)
        account_exist = False
        if emails:
            account_exist = True
        if phone_no:
            account_exist = True
        if account_exist:
            # return JsonResponse({"success": False, "message": "Account already existed with following info"})
            res = serializers.ValidationError({'message':'Account already existed with following info', 'status_code':'400'})
            raise res

        else:
            # request.data._mutable =True
            # password = request.data['password']
            # request.session.delete('email_otp')
            # request.session.delete('phone_otp')
            Profile.objects.create_user(
                email=email,
                phone=phone,
                invitation_code=invitation_code,
                password=password
            )
            if status.HTTP_201_CREATED:
                return JsonResponse({"success": True, "message": "Account Created"})
            elif status.HTTP_500_INTERNAL_SERVER_ERROR:
                # return JsonResponse({"success": False, "message": "Server Error"})
                res = serializers.ValidationError({'message':'Internal Server Error', 'status_code':'500'})
                raise res
            # return JsonResponse({"msg": "User Account created"})

    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def userLogin(request):
        password = request.GET['password']
        operation = request.GET['operation']
        otp = request.GET['otp']
        if '@' in str(operation):
            email = request.session.get('email_otp')
            if int(otp) != email:
                # return JsonResponse({"success": False, "message": "Email Otp Not Verified"})
                res = serializers.ValidationError({'message':'Invalid  otp', 'status_code':'400'})
                # res.status_code = 200
                raise res
            try:
                user = Profile.objects.get(email=operation)
            except:
                # return JsonResponse({"success": False, "message": "User Record Not Found"})
                res = serializers.ValidationError({'message':'User not exists, please signup first.', 'status_code':'400'})
                res.status_code = 200
                raise res
        else:
            phone = request.session.get('otp')
            if int(otp) != phone:
                res = serializers.ValidationError({'message':'Invalid  otp', 'status_code':'400'})
                # res.status_code = 200
                raise res
                # return JsonResponse({"success": False, "message": "Phone Otp Not Verified"})
            try:
                user = Profile.objects.get(phone=operation)
            except:
                # return JsonResponse({"success": False, "message": "User Record Not Found"})
                res = serializers.ValidationError({'message':'User not exists, please signup first.', 'status_code':'400'})
                # res.status_code = 200
                raise res
        if user:
            if check_password(password, user.password):
                # user.generate_jwt_token()
                tokens = user.token
                data = {"access_tokens": tokens, "email": user.email}
                return JsonResponse({"data": data, "message": "Successfull Login"})
            else:
                res = serializers.ValidationError({'message':'Invalid password', 'status_code':'400'})
                # res.status_code = 200
                raise res
                # return JsonResponse({"success": False, "message": "Login Failed"})
        else:
            if status.HTTP_500_INTERNAL_SERVER_ERROR:
                # return JsonResponse({"success": False, "message": "Internal Server Error"})
                res = serializers.ValidationError({'message':'Internal Server Error', 'status_code':'500'})
                # res.status_code = 200
                raise res

            else:
                # return JsonResponse({"success": False, "message": "Invalid email or password"})
                res = serializers.ValidationError({'message':'Invalid email or password', 'status_code':'400'})
                # res.status_code = 200
                raise res

    @api_view(['POST'])
    @permission_classes([permissions.AllowAny])
    def change_password(request):
        password = request.GET['password']
        email = request.session.get('email')
        phone = request.session.get('phone')

        user = Profile.objects.filter(email=email).filter(phone=phone)
        user.update(password=make_password(password))
        if user:
            if status.HTTP_200_OK:
                return JsonResponse({"success": True, "message": "Password Changed"})
        elif len(user) == 0:
            # return JsonResponse({"success": False, "message": "User Record Not Found"})
            res = serializers.ValidationError({'message':'User not exists, please signup first.', 'status_code':'400'})
            # res.status_code = 200
            raise res
        else:
            res = serializers.ValidationError({'message':'Internal Server Error', 'status_code':'500'})
            # res.status_code = 200
            raise res
