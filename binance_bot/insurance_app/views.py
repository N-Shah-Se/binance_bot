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
from .models import Insurance


# Create your views here.


class KycUser(APIView):
    # permission_classes = (AllowOptionsAuthentication,)
    # permission_classes = (permission_classes.IsAuthenticated,)
    @api_view(['POST'])
    @permission_classes([permissions.AllowAny])
    def add_data(request):
        try:
            authenticated = request.session.get('authenticated')
            if authenticated==False:
                return JsonResponse({"status": False, "message": "Please Login To Use The App"})
            fname = request.data['first_name']
            lname = request.data['last_name']
            gender = request.data['gender']
            dob = request.data['dob']
            email = request.data['email']
            phone = request.data['phone']
            occupation = request.data['occupation']

            house_address = request.data['house_address']
            city = request.data['city']
            state = request.data['state']
            pin_code = request.data['pin_code']
            aadhar_card_no = request.data['aadhar_card_no']
            ### front image
            pan_card_no = request.data['pan_card_no']
            gstn_no = request.data['gstn_no']
            #### Card image
            nominee_name = request.data['nominee_name']
            nominee_age = request.data['nominee_age']
            nominee_relation = request.data['nominee_relation']
            aadhar_no = request.data['aadhar_no']
            aadhar_pan = request.data['aadhar_pan']
            self_data = request.data['self']
            death = request.data['death']
            permanent_total_disable = request.data['permanent_total_disable']
            permanent_partial_disable = request.data['permanent_partial_disable']
            temporary_total_disable = request.data['temporary_total_disable']
            # login_email = request.user.email
            login_email='nasir@gmail.com'

            Insurance.objects.create(first_name=fname,last_name=lname,gender=gender,dob=dob,email=email,phone=phone,occupation=occupation,house_address=house_address,city=city,state=state,pin_code=pin_code,aadhar_card_no=aadhar_card_no,pan_card_no=pan_card_no,gstn_no=gstn_no,nominee_name=nominee_name,nominee_age=nominee_age,nominee_relation=nominee_relation,aadhar_no=aadhar_no,aadhar_pan=aadhar_pan,self_data=self_data,death=death,permanent_total_disable=permanent_total_disable,permanent_partial_disable=permanent_partial_disable,temporary_total_disable=temporary_total_disable,login_email=login_email)
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
