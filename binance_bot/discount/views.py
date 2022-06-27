from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from rest_framework import views, status, serializers
from rest_framework import response, permissions
from rest_framework.decorators import permission_classes
from django.core.exceptions import ObjectDoesNotExist
from .models import DiscountBonus, DirectBonus,Referal
from user_account.models import Account


# Create your views here.
class GFM:
   
    i=107

class discount(APIView):
    # permission_classes = (AllowOptionsAuthentication,)
    # permission_classes = (permission_classes.IsAuthenticated,)
    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def bonus_discount(request):
        try:
            is_company_referal = Accounts.objects.filter(invitation_code="GFM2803")
            if is_company_referal:
                account_balance = request.GET['account_balance']
                # ref_code = request.GET['ref_code']
                GFM.i+=1
                total_per = (float(account_balance) * 5 )/100
                ref_code = 'GFM'+str(GFM.i)
                gfm_code = ref_code + '/G ' + str(total_per)
                tds = (total_per * 5)/100
                magic_bonus = (total_per*10)/100
                balance = total_per - (tds + magic_bonus)
                DiscountBonus.objects.create(tds=tds,ref_code=ref_code,account=request.user,magic_bonus=magic_bonus,balance=balance)
                # Referal.objects.create(account=request.user,referal_code=ref_code)

        except Exception as e:
            return JsonResponse({"success":False , "message":f"{e}" })
            # res = serializers.ValidationError({'message':f'{e}', 'status_code':'500'})
            # # res.status_code = 200
            # raise res
        # user = Profile.objects.get(email=request.user.email)
        data = {"ref_no":gfm_code,"tds":"{:.2f}".format(tds),"magic_bonus":"{:.2f}".format(magic_bonus),"balance":"{:.2f}".format(balance)}
        return JsonResponse({"success":True , "message":data })


    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def direct_discount(request):
        try:
            account_balance = request.GET['account_balance']
            referal_code = request.GET['referal_code']
            is_exist = Referal.objects.filter(ref_code=referal_code)
            if is_exist:
                # GFM.i+=1
                total_per = (float(account_balance) * 30 )/100
                gfm_code = referal_code+ '/G ' + str(total_per)
                tds = (total_per * 5)/100
                magic_bonus = (total_per*10)/100
                balance = total_per - (tds + magic_bonus)
                DirectBonus.objects.create(tds=tds,ref_code=gfm_code,account=request.user,magic_bonus=magic_bonus,balance=balance)
        except Exception as e:
            return JsonResponse({"success":False , "message":f"{e}" })
            # res = serializers.ValidationError({'message':f'{e}', 'status_code':'500'})
            # # res.status_code = 200
            # raise res
        # user = Profile.objects.get(email=request.user.email)
        data = {"ref_no":gfm_code,"tds":"{:.2f}".format(tds),"magic_bonus":"{:.2f}".format(magic_bonus),"balance":"{:.2f}".format(balance)}
        return JsonResponse({"success":True , "message":data })


class referal_code(APIView):
    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def get_referal_code(request):
        try:
            email = request.GET['email']
            ref_code = Referal.objects.get(account=Account.objects.get(email=email)).referal_code
            print(ref_code)
        except Exception as e:
            return JsonResponse({"success":False , "message":f"{e}" })
        data = {"ref_no":ref_code}
        return JsonResponse({"success":True , "message":data })
            

