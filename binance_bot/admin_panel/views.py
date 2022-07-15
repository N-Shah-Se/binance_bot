from django.shortcuts import render,redirect
from django.http import HttpResponse
from user_account.models import Account
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate ,login  , logout
from django.contrib.auth.decorators import  login_required
from .decorators import notLoggedUsers , allowedUsers, forAdmins
from django.contrib.auth.models import Group
from manual_trading.models import BotUser
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password
import requests
from django.conf import settings
from user_account.views import send_otp
from kyc_app.models import KYC
from binance.exceptions import BinanceAPIException,BinanceOrderException,BinanceRequestException,BinanceOrderMinAmountException,BinanceOrderMinPriceException,BinanceOrderMinTotalException,BinanceOrderUnknownSymbolException,BinanceOrderInactiveSymbolException
from binance.client import Client
from binance.enums import *

@login_required(login_url='login')
# @allowedUsers(allowedGroups=['admin'])
# @forAdmins
def home(request):

    return render(request , 'index.html',{})


@notLoggedUsers
def userLogin(request):

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request ,email=email, password=password)

            print(f"{user}")
            if user is not None:
                login(request, user)
                try:
                    user = Account.objects.get(email=email)
                    request.session['name'] = user.first_name + ' ' + user.last_name
                    request.session['image'] = 'https://nshah.pythonanywhere.com/media/'+str(user.image_url)
                except:
                    print("s")
                print(f"{user}")
                return redirect('home')
            else:
                messages.info(request, 'Credentials error')

        context = {}

        return render(request , 'sheet/login.html', context )


@login_required(login_url='login')
def userLogout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
# @allowedUsers(allowedGroups=['customer'])
def accounts(request):
    users = Account.objects.all()
    return render(request , 'sheet/accounts.html', {"users":users})

@login_required(login_url='login')
# @allowedUsers(allowedGroups=['customer'])
def bot_users(request):
    try:
        bot_users = BotUser.objects.all()
        user_data = []
        # bot_data = bot_users
        for i in bot_users:
            users = Account.objects.get(email=i.user)
            user={}
            user['name'] = users.first_name + ' ' + users.last_name
            user['phone'] = users.phone
            user['email'] = users.email
            user_data.append(user)
        return render(request, 'sheet/bot_user.html', {"bot_users":user_data})
    except Exception as e:
        bot_users = {}
        return render(request , 'sheet/bot_user.html', {"bot_users":user_data})

def order(email,side,api_key,secret_key):
    try:
        client = Client(api_key, secret_key)
        current_price = float(client.get_symbol_ticker(symbol=currency)["price"])
        current_price =float('{:.8f}'.format(current_price))
        # request.session['client'] = client

        new_order = client.create_order(
        symbol=currency,
        side=side,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=30,
        price=current_price)
    # except BinanceAPIException as e:
    #     return f"{e}"
    # except BinanceOrderException as e:
    #     return f"{e}"
    # except BinanceRequestException as e:
    #     return f"{e}"
    # except BinanceOrderMinAmountException as e:
    #     return f"{e}"
    # except BinanceOrderMinPriceException as e:
    #     return f"{e}"
    # except BinanceOrderMinTotalException as e:
    #     return f"{e}"
    # except BinanceOrderUnknownSymbolException as e:
    #     return f"{e}"
    # except BinanceOrderInactiveSymbolException as e:
    #     return f"{e}"
    except:
        return ""
    return new_order

@login_required(login_url='login')
# @allowedUsers(allowedGroups=['customer'])
def place_order(request):
    if request.method == 'POST':
        try:
            selected_values = request.POST.getlist('check')
            failed_for= []
            for email in selected_values:
                bot_users = BotUser.objects.get(user=email)
                data = {}
                side = ''
                if request.POST.get("buy"):
                    side = "BUY"
                    # data['resp'] = order(email,"BUY",bot_users.api_key,bot_users.secret_key)
                elif request.POST.get("sell"):
                    side = "SELL"
                # client = Client(bot_users.api_key, bot_users.secret_key)
                # currency = 'XRPUSDT'
                # current_price = float(client.get_symbol_ticker(symbol=currency)["price"])
                # current_price =float('{:.8f}'.format(current_price))
                # # request.session['client'] = client
                # new_order = client.create_order(
                # symbol=currency,
                # side=side,
                # type=ORDER_TYPE_LIMIT,
                # timeInForce=TIME_IN_FORCE_GTC,
                # quantity=30,
                # price=current_price)
                order(email,side,bot_users.api_key,bot_users.secret_key)
                # if new_order:
                #     pass
                # else:
                #     data['email'] = email
                #     data['error'] = new_order
                #     failed_for.append(data)
                # if failed_for:
                #     return redirect('home')
            return redirect('bot_users')
        except Exception as ex:
            return redirect('home')
            # print(f'hello user{ex}')
    return redirect('bot_users')


# @login_required(login_url='login')
# @allowedUsers(allowedGroups=['customer'])
def forgot_password(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            # phone = request.POST.get('phone')
            request.session['email'] = email
            user = Account.objects.filter(email=email)
            if user:
                email_otp = random.randint(100000, 999999)
                phone_otp = random.randint(100000, 999999)
                request.session['email_otp'] = email_otp
                request.session['phone_otp'] = phone_otp
                email_message = f"Dear Prime User,\n Your OTP for forgot password to G Flight MODE is {email_otp}. if this was not you, please inform support or info@gflightmode.com. Please do not share this OTP\nRegards GFM TeamOTP"
                phone_message = f"Dear Prime User,\n Your OTP for forgot password to G Flight MODE is {phone_otp}. if this was not you, please inform support or info@gflightmode.com. Please do not share this OTP\nRegards GFM TeamOTP"
                # send_otp(phone,phone_message)
                send_mail(
                    'Email Verification OTP',
                    email_message,
                    'settings.EMAIL_HOST_USER',
                    [email],
                    fail_silently=False, )
                return render(request, 'sheet/email_otp.html')
        except Exception as ex:
            print(f"{ex}")

    return render(request, 'sheet/forgot_password.html')

def email_otp(request):
    if request.method == 'POST':
        email_otp = request.POST.get('email_otp')
        e_otp = request.session.get('email_otp')
        # phone_otp = int(request.POST.get('phone_otp'))
        # p_otp = int(request.session.get('phone_otp'))
        # if email_otp == e_otp:
        # print(email_otp,e_otp)
        if int(email_otp)== int(e_otp):
            print(email_otp, e_otp)
            data = {}
            request.session.delete('email_otp')
            request.session.delete('phone_otp')
            return render(request, 'sheet/change_password.html')
    return render(request, 'sheet/email_otp.html')

    #     # context = []
    #     # for i in users:
    #     #     user = {}
    #     #     user['phone'] = i['phone']
    #     #     user['email'] = i['email']
    #     #     user['invitation_code'] = i['invitation_code']
    #     #     context.append(user)
    #     return render(request, 'sheet/bot_user.html', {"bot_users":bot_data})
    # except Exception as e:
    #     bot_users = {}
    # return render(request , 'sheet/bot_user.html', {"bot_users":bot_data})

def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if password == re_password:
            email = request.session.get('email')
            user = Account.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return render(request, 'sheet/login.html')
    return render(request, 'sheet/change_password.html')



@login_required(login_url='login')
def profileInfo(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
         form = CustomerForm(request.POST , request.FILES, instance=customer)
         if form.is_valid():
             form.save()
    context = {'form':form}


    return render(request , 'bookstore/profile_info.html', context )


@login_required(login_url='login')
# @allowedUsers(allowedGroups=['customer'])
def kyc_user_update(request):
    try:
        kyc_users = KYC.objects.all()
        # bot_data = bot_users
        # for i in bot_users:
        #     users = Account.objects.filter(email=i['email'])
        #     user={}
        #     user['phone'] = users.phone
        #     user['email'] = users.email
        return render(request, 'sheet/kyc_user.html', {"kyc_user":kyc_users})
    except Exception as e:
        # kyc_users = {}
        # print("hhhhh")
        return render(request , 'sheet/kyc_user.html')


@login_required(login_url='login')
# @allowedUsers(allowedGroups=['customer'])
def kyc_details(request,id):

    # try:
    id = int(id)
    kyc_users = KYC.objects.get(id=id)
        # bot_data = bot_users
        # for i in bot_users:
        #     users = Account.objects.filter(email=i['email'])
        #     user={}
        #     user['phone'] = users.phone
        #     user['email'] = users.email
    return render(request, 'sheet/kyc_details.html', {"kyc_users":kyc_users})
    # except Exception as e:
        # return render(request , 'sheet/kyc_user.html')


@login_required(login_url='login')
# @allowedUsers(allowedGroups=['customer'])
def kyc_change_status(request,id,status):

    try:
        kyc_users = KYC.objects.get(id=id)
        kyc_users.kyc_status = status
        kyc_users.save()
        # bot_data = bot_users
        # for i in bot_users:
        #     users = Account.objects.filter(email=i['email'])
        #     user={}
        #     user['phone'] = users.phone
        #     user['email'] = users.email
        return redirect('kyc_user_update')
    except Exception as e:
        kyc_users = {}
        return redirect('home')















