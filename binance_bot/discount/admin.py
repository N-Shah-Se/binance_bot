from django.contrib import admin
from .models import DiscountBonus,Referal,LeadershipBonus,LeadershipInfo,special_days,ReTopUpBonus, StarCount
# Register your models here.
admin.site.register(DiscountBonus)
admin.site.register(Referal)
admin.site.register(LeadershipBonus)
admin.site.register(LeadershipInfo)
admin.site.register(special_days)
admin.site.register(ReTopUpBonus)
admin.site.register(StarCount)