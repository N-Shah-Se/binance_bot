import re
import os
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from rest_framework import views, status, serializers
from rest_framework import response, permissions
from rest_framework.decorators import permission_classes
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from .models import Nominee as Nominee_Model


# Create your views here.


class Nominee(APIView):
    # permission_classes = (AllowOptionsAuthentication,)
    # permission_classes = (permission_classes.IsAuthenticated,)
    @api_view(['POST'])
    @permission_classes([permissions.AllowAny])
    def add_data(request):
        try:
            authenticated = request.session.get('authenticated')
            if authenticated==False:
                return JsonResponse({"status": False, "message": "Please Login To Use The App"})
            nominee_name = request.data['nominee_name']
            nominee_age = request.data['nominee_age']
            nominee_relation = request.data['nominee_relation']
            aadhar_no = request.data['aadhar_no']
            aadhar_pan = request.data['aadhar_pan']
            account_number = request.data['account_number']
            account_holder = request.data['account_holder']
            ifsc_code = request.data['ifsc_code']
            rbi_bank = request.data['rbi_bank']
            login_email='nasir@gmail.com'

            Nominee_Model.objects.create(nominee_name=nominee_name,nominee_age=nominee_age,nominee_relation=nominee_relation,aadhar_no=aadhar_no,aadhar_pan=aadhar_pan,
            account_number=account_number,account_holder=account_holder,ifsc_code=ifsc_code,rbi_bank=rbi_bank,login_email=login_email)
            # user.save()
        except Exception as e:
            return JsonResponse({"success":False , "message":f"{e}" })
            # res = serializers.ValidationError({'message':f'{e}', 'status_code':'500'})
            # # res.status_code = 200
            # raise res
        # user = Profile.objects.get(email=request.user.email)
        # data = {"first_name":user.first_name,"last_name":user.last_name,"username":user.username,"image":f"nshah.pythonanywhere.com/media/{user.image_url}"}
        return JsonResponse({"success":True , "message":"Successfully saved data" })

    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def get_status(request):
        authenticated = request.session.get('authenticated')
        if authenticated==False:
            return JsonResponse({"status": False, "message": "Please Login To Use The App"})
        data = {}
        try:
            email = request.user.email
            kyc_status = KYC.objects.get(login_email=email)
            if kyc_status:
                data = {"kyc_status":kyc_status.kyc_status}
        except Exception as e:
            return JsonResponse({"status":False , "message":"You have not submitted KYC form." })
            # res = serializers.ValidationError({'message':f'{e}', 'status_code':'500'})
            # # res.status_code = 200
            # raise res
        # user = Profile.objects.get(email=request.user.email)
        # data = {"first_name":user.first_name,"last_name":user.last_name,"username":user.username,"image":f"nshah.pythonanywhere.com/media/{user.image_url}"}
        return JsonResponse({"success":True , "data":data })
