import email
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from rest_framework import views, status, serializers
from rest_framework import response, permissions
from rest_framework.decorators import permission_classes
from django.core.exceptions import ObjectDoesNotExist
from .models import DiscountBonus, DirectBonus,Referal,special_days,LeadershipInfo,LeadershipBonus, ReTopUpBonus, StarCount
from user_account.models import Account
from datetime import date
from django.db.models import Q  
from django.db.models import Sum


# Create your views here.
class GFM:
    i=107

class discount(APIView):
    # permission_classes = (AllowOptionsAuthentication,)
    # permission_classes = (permission_classes.IsAuthenticated,)
    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def discount_bonus(request):
        try:
            referal_code = request.GET['referal_code']
            email = request.GET['email']
            
            if referal_code=='GFM2803':
                account = Account.objects.get(email=email)
            # is_company_referal = Accounts.objects.filter(invitation_code="GFM2803")
                is_special_day = special_days.objects.filter(special_date=date.today())
                if  is_special_day:
                    account_balance = request.GET['account_balance']
                    # ref_code = request.GET['ref_code']
                    GFM.i+=1
                    total_per = (float(account_balance) * 5 )/100
                    ref_code = 'GFM'+str(GFM.i)
                    gfm_code = ref_code + '/G ' + str(total_per)
                    tds = (total_per * 5)/100
                    magic_bonus = (total_per*10)/100
                    balance = total_per - (tds + magic_bonus)
                    DiscountBonus.objects.create(tds=tds,ref_code=ref_code,account=account,magic_bonus=magic_bonus,balance=balance, bonus_type="discount", remark=is_special_day[0].title)
                # Referal.objects.create(account=request.user,referal_code=ref_code)
            else:
                gfm_code=None
                tds=0
                magic_bonus=0
                balance=0

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
    def direct_bonus(request):
        try:
            account_balance = request.GET['account_balance']
            referal_code = request.GET['referal_code']
            email = request.GET['email']
            new_user_email = request.GET['created_user_email']
            is_exist = Referal.objects.filter(referal_code=referal_code)
            if is_exist:
                # GFM.i+=1
                account = Account.objects.get(email=email)
                total_per = (float(account_balance) * 30 )/100
                ref_code = 'GFM'+str(GFM.i)
                gfm_code = ref_code+ '/G ' + str(total_per)
                tds = (total_per * 5)/100
                magic_bonus = (total_per*10)/100
                balance = total_per - (tds + magic_bonus)
                for_account = Account.objects.get(email=new_user_email)
                remark_direct = "Bonus By "+ for_account.first_name +"s GFM Prime"
                DiscountBonus.objects.create(tds=tds,ref_code=gfm_code,account=account,magic_bonus=magic_bonus,balance=balance, bonus_type="direct", remark=remark_direct)
        except Exception as e:
            return JsonResponse({"status":False , "message":f"{e}" })
            # res = serializers.ValidationError({'message':f'{e}', 'status_code':'500'})
            # # res.status_code = 200
            # raise res
        # user = Profile.objects.get(email=request.user.email)
        data = {"ref_no":gfm_code,"tds":"{:.2f}".format(tds),"magic_bonus":"{:.2f}".format(magic_bonus),"balance":"{:.2f}".format(balance)}
        return JsonResponse({"status":True , "message":data })


    @api_view(['GET'])
    @permission_classes([permissions.AllowAny])
    def user_bonus(request):
        try:
            user_email = request.GET['email']
            bonus = request.GET['bonus']
            account = Account.objects.get(email=user_email)
            if bonus=='magic':
                data = DiscountBonus.objects.filter(Q(account=account) and Q(re_top_up_status=False)).values()
            else:
                data = DiscountBonus.objects.filter(Q(account=account) and Q(bonus_type=bonus)).values()
            #print(data)
        except Exception as e:
            return JsonResponse({"success":False , "message":f"{e}" })
        return JsonResponse({"success":True , "message":list(data) })



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



class leadership_bonus(APIView):
    permission_classes = [permissions.AllowAny]
    def maintain_leadership( self, current_user,current_user_account, bonus_type, referal_code, depth_count, **kwargs):
        if referal_code == 'GFM2803':
            return kwargs
        else:
            direct_count=0
            indirect_count=0
            total_count=0
            try:
                current_user_info= LeadershipInfo.objects.filter(account=current_user).latest('created')
                indirect_count = int(current_user_info.indirect_count)
                direct_count = int(current_user_info.direct_count)
                total_count = int(current_user_info.total_count) +1
                if bonus_type =="Indirect":
                    indirect_count = int(current_user_info.indirect_count) +1
                else:
                    direct_count = int(current_user_info.direct_count) +1
            except LeadershipInfo.DoesNotExist:
                total_count = 1
                if bonus_type =="Indirect":
                    indirect_count = 1
                else:
                    direct_count = 1
            leadership_bonus =LeadershipBonus.objects.filter(target__lte=total_count)
            
            if leadership_bonus.count()>0:
                required_index = leadership_bonus.count()-1
                rank_obj = leadership_bonus[int(required_index)].incentive_percentage
                bonus_percent = leadership_bonus[int(required_index)].incentive_percentage
                rank = leadership_bonus[int(required_index)].rank
            else:
                rank_obj = LeadershipBonus.objects.filter(rank="Blue Sapphire")
                bonus_percent = rank_obj[0].incentive_percentage
                rank = rank_obj[0].rank   
            next_user = Referal.objects.get(referal_code=current_user.invitation_code).account
            gen_id = LeadershipInfo.objects.create(account=current_user,for_account=current_user_account,direct_count=direct_count, indirect_count= indirect_count, total_count=total_count, rank=LeadershipBonus.objects.get(rank=rank))
            current_user_leadership_info = [depth_count,bonus_percent, gen_id.id]
            #print(depth_count)
            kwargs[str(depth_count)]=current_user_leadership_info
            
            #print(kwargs)
            bonus_type = "Indirect"
            depth_count += 1
        return self.maintain_leadership(next_user,current_user_account, bonus_type, current_user.invitation_code, depth_count, **kwargs)
        
    def getList(dict):
        return dict.keys()
    def get(self,request):
        try:
            referal_code = request.GET['referal_code']
            account_balance = request.GET['account_balance']
            created_account = request.GET['new_user_email']
            current_user = Referal.objects.get(referal_code=referal_code).account
            current_user_account = Account.objects.get(email=created_account)

            bonus_type="Direct"
            depth_count = 1
            kwargs = {}
            data=leadership_bonus.maintain_leadership(self,current_user,current_user_account, bonus_type, referal_code,depth_count, **kwargs)
            print(sorted (data.keys()).sort(reverse=True))
            for x, y in data.items():
                print(x, y)
            for i in sorted(data.keys()) :
                print(i)
                if int(i)==1:
                    commission_low = data[str(i)][1]
                    total_per = (float(account_balance) * commission_low )/100
                    gfm_code = referal_code+ '/G ' + str(total_per)
                    tds = (total_per * 5)/100
                    magic_bonus = (total_per*10)/100
                    balance = total_per - (tds + magic_bonus)
                    print(balance)
                    print("commission low")
                else:
                    commission_low = data[str(int(i)-1)][1]
                    commission_high = data[str(int(i))][1]
                    commission_diff = commission_high-commission_low
                    total_per = (float(account_balance) * commission_diff )/100
                    gfm_code = referal_code+ '/G ' + str(total_per)
                    tds = (total_per * 5)/100
                    magic_bonus = (total_per*10)/100
                    balance = total_per - (tds + magic_bonus)
                    print(balance)
                    print("commission_high")
                remark_user = Account.objects.get(email=created_account)
                remark = "Bonus by "+remark_user.first_name+"s GFM Team"
                if balance>0:
                    DiscountBonus.objects.create(tds=tds,ref_code=gfm_code,account=current_user,magic_bonus=magic_bonus,balance=balance, bonus_type="leadership", remark=remark)

            return JsonResponse({"success":True })
        except Exception as e:
            return JsonResponse({"success":False, "message":f"{e}"})



class re_top_up_bonus(APIView):
    permission_classes = [permissions.AllowAny]
    def maintain_leadership( self, current_user,current_user_account, bonus_type, referal_code, depth_count, **kwargs):
        if referal_code == 'GFM2803':
            return kwargs
        else:
            direct_count=0
            indirect_count=0
            total_count=0
            try:
                current_user_info= LeadershipInfo.objects.filter(account=current_user).latest('created')
                total_count = int(current_user_info.total_count)
                print(total_count)
            except LeadershipInfo.DoesNotExist:
                total_count = 0
               
            leadership_bonus =LeadershipBonus.objects.filter(target__gte=total_count)
            rank = leadership_bonus[0].rank
                
            next_user = Referal.objects.get(referal_code=current_user.invitation_code).account
            re_top_up_percentage = ReTopUpBonus.objects.get(rank=rank).incentive_percentage
            #gen_id = LeadershipInfo.objects.create(account=current_user,for_account=current_user_account,direct_count=direct_count, indirect_count= indirect_count, total_count=total_count, rank=LeadershipBonus.objects.get(rank=rank))
            current_user_leadership_info = [str(current_user.email), str(rank), re_top_up_percentage]
            print(current_user_leadership_info)
            #print(depth_count)
            kwargs[str(depth_count)]=current_user_leadership_info
            
            #print(kwargs)
            bonus_type = "Indirect"
            depth_count += 1
        return self.maintain_leadership(next_user,current_user_account, bonus_type, current_user.invitation_code, depth_count, **kwargs)
        
    def getList(dict):
        return dict.keys()
    def get(self,request):
        try:
            referal_code = request.GET['referal_code']
            account_balance = request.GET['account_balance']
            created_account = request.GET['created_user_email']
            current_user = Referal.objects.get(referal_code=referal_code).account
            current_user_account = Account.objects.get(email=created_account)

            bonus_type="Direct"
            depth_count = 1
            kwargs = {}
            data=re_top_up_bonus.maintain_leadership(self,current_user,current_user_account, bonus_type, referal_code,depth_count, **kwargs)
            print(data)
            StarCount.objects.create(account=current_user)
            for i in sorted(data.keys()) :
                print(i)
                if int(i)==1:
                    commission_low = data[str(i)][2]
                    total_per = (float(account_balance) * commission_low )/100
                    gfm_code = referal_code+ '/G ' + str(total_per)
                    tds = 0
                    magic_bonus = 0
                    balance = total_per - (tds + magic_bonus)
                    print(balance)
                    print("commission low " + str(commission_low))
                else:
                    commission_low = data[str(int(i)-1)][2]
                    commission_high = data[str(int(i))][2]
                    commission_diff = commission_high-commission_low
                    total_per = (float(account_balance) * commission_diff )/100
                    gfm_code = referal_code+ '/G ' + str(total_per)
                    tds = 0
                    magic_bonus = 0
                    balance = total_per - (tds + magic_bonus)
                    print(balance)
                    print("commission_high" + str(commission_high))
                remark_user = Account.objects.get(email=created_account)
                remark = "Bonus by "+remark_user.first_name+"s GFM Re-Topup"
                if balance>0:
                    DiscountBonus.objects.filter(Q(account=account) and Q(re_top_up_status=False)).update(re_top_up_status=True)
                    DiscountBonus.objects.create(tds=tds,ref_code=gfm_code,account=current_user,magic_bonus=magic_bonus,balance=balance, bonus_type="retopup", remark=remark)
                data_calculate_total_magic = DiscountBonus.objects.filter(Q(account=current_user) and Q(re_top_up_status=False)).aggregate(Sum('magic_bonus'))
                print(data_calculate_total_magic['magic_bonus__sum'])
            return JsonResponse({"success":True, "message":data })
        except Exception as e:
            return JsonResponse({"success":False, "message":f"{e}"})

