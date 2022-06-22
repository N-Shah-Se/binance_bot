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
from .models import KYC


# Create your views here.


class KycUser(APIView):
    # permission_classes = (AllowOptionsAuthentication,)
    # permission_classes = (permission_classes.IsAuthenticated,)
    @api_view(['POST'])
    @permission_classes([permissions.AllowAny])
    def add_data(request):
        try:
            name = request.data['name']
            fname = request.data['fname']
            gender = request.data['gender']
            dob = request.data['dob']
            house_address = request.data['house_address']
            city = request.data['city']
            state = request.data['state']
            pin_code = request.data['pin_code']
            cnic = request.data['cnic']
            ### front image
            cnic_front = request.FILES['cnic_front']
            file_name_split = os.path.split(cnic_front.name)
            image_ext = file_name_split[1].split('.')[-1]
            cnic_front_img = request.user.phone+"."+image_ext
            request.data._mutable = True
            request.FILES['cnic_front'].name = cnic_front_img
            request.data._mutable = False
            ###### back image
            cnic_back = request.FILES['cnic_back']
            file_name_split = os.path.split(cnic_back.name)
            image_ext = file_name_split[1].split('.')[-1]
            cnic_back_img = request.user.phone+"."+image_ext
            request.data._mutable = True
            request.FILES['cnic_back'].name = cnic_back_img
            request.data._mutable = False
            #### Card image
            card_no = request.data['card_no']
            card_image = request.FILES['card_image']
            file_name_split = os.path.split(card_image.name)
            image_ext = file_name_split[1].split('.')[-1]
            card_img = request.user.phone+"."+image_ext
            request.data._mutable = True
            request.FILES['card_image'].name = card_img
            request.data._mutable = False
            account_no = request.data['account_no']
            account_holder = request.data['account_holder']
            ifsc_code = request.data['ifsc_code']
            bank_name = request.data['bank_name']
            email = request.data['email']
            phone = request.data['phone']

            user = KYC.objects.create(name=name,fname=fname,gender=gender,dob=dob,email=email,phone=phone,house_address=house_address,city=city,state=state,pin_code=pin_code,cnic=cnic,cnic_front=cnic_front,cnic_back=cnic_back,card_no=card_no,card_image=card_image,account_no=account_no,account_holder=account_holder,ifsc_code=ifsc_code,bank_name=bank_name)
            # user.save()

        except Exception as e:
            return JsonResponse({"success":False , "message":f"{e}" })
            # res = serializers.ValidationError({'message':f'{e}', 'status_code':'500'})
            # # res.status_code = 200
            # raise res
        # user = Profile.objects.get(email=request.user.email)
        # data = {"first_name":user.first_name,"last_name":user.last_name,"username":user.username,"image":f"nshah.pythonanywhere.com/media/{user.image_url}"}
        return JsonResponse({"success":True , "message":"Successfully saved data" })



