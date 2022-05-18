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


class UserRegisteration(APIView):
    @api_view(['GET'])
    def get_phone_otp(request, phone):
        phone = phone
        request.session['phone'] = phone
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        message = f'OTP \n {otp}'
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
    def get_email_otp(request, email):
        otp = random.randint(100000, 999999)
        request.session['email_otp'] = otp
        request.session['email'] = email
        message = f'your otp is {otp}'
        send_mail(
            'Email Verification OTP',
            message,
            'settings.EMAIL_HOST_USER',
            [email],
            fail_silently=False,)
        return JsonResponse({"msg": "OTP send to your email successfully"})

    @api_view(["POST"])
    def email_verification(request):
        user_otp = request.GET['otp']
        otp = request.session['email_otp']
        if int(user_otp) == otp:
            return JsonResponse({"msg": "Email Verified"})
        else:
            return JsonResponse({"msg": "Email Not Verified"})

    @api_view(['POST'])
    def add_user(request):
        password = request.GET['password']
        phone_otp = request.GET['phone_otp']
        email_otp = request.GET['email_otp']
        invitation_code = request.GET['invitation_code']
        email = request.session.get('email_otp')
        phone = request.session.get('otp')
#        otp = request.session['email_otp']
        if int(email_otp) == email and int(phone_otp) == phone:
            pass
        elif int(email_otp) != email:
            return JsonResponse({"msg": f"Email Not Verified{email}{email_otp}"})
        elif int(phone_otp) != phone:
            return JsonResponse({"msg": f"Wrong OTP{phone}{phone_otp}"})
        hash_pwd = make_password(password)
        emails = Profile.objects.filter(email=email)
        phone_no = Profile.objects.filter(phone=phone)
        account_exist = False
        #print(email, phone)
        if emails:
            account_exist = True
        if phone_no:
            account_exist = True

        if account_exist:
            return JsonResponse({"msg": "Account already exist"})
        else:
            Profile.objects.create(
                phone=phone,
                email=email,
                invitation_code=invitation_code,
                password=hash_pwd
            )
            return JsonResponse({"msg": "User Account created"})

    @api_view(['GET'])
    def userLogin(request):
        password = request.GET['password']
        operation = request.GET['operation']
        otp = request.GET['otp']
        if '@' in str(operation):
            email = request.session.get('email_otp')
            if int(otp) != email:
                return JsonResponse({"msg": f"Email Not Verified{email}{otp}"})
            user= Profile.objects.filter(email=operation)
        else:

            phone = request.session.get('otp')
            if int(otp) != phone:
                return JsonResponse({"msg": f"Wrong OTP{phone}{otp}"})
            user = Profile.objects.filter(phone=operation)
<<<<<<< HEAD
=======
	#user = Profile.objects.filter(email=email)
>>>>>>> d1a92f2e744d498e0343b7316cf3daa45094e204
        user_password = ""
        for ps in user:
            user_password = ps.password
        print(f"{user}")
        if user_password:
            if check_password(password, user_password):
                return JsonResponse({"msg": "Login Successfully"})
            else:
                return JsonResponse({"msg": "Login Failed"})
        else:
            return JsonResponse({"msg": "Login Failed"})

    @api_view(['POST'])
    def change_password(request):
        password = request.GET['password']
        email = request.session.get('email')
        phone = request.session.get('phone')
        user = Profile.objects.filter(email=email).filter(phone=phone)
        user.update(password=make_password(password))
        return JsonResponse({"msg": "Password Changed"})
