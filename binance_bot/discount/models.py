from django.db import models

# Create your models here.
from django.db import models
import uuid
# from accounts.models import Referral
from user_account.models import Account

# Create your models here.

class ReferalIncrement(models.Model):
    referal_code = models.IntegerField()

class Referal(models.Model):
    account = models.OneToOneField(Account, on_delete=models.RESTRICT, null=True, blank=True)
    # unique code Ex: GFM107
    referal_code = models.CharField(max_length=200, null=True, blank=True)

class DiscountBonus(models.Model):

    account = models.OneToOneField(Account, on_delete=models.RESTRICT, null=True, blank=True)

    # OneToOne relatioship
    # To delete it you will have to delete all objects that reference it manually. RESTRICT
    # to='funds.Payment' used to avoid Circular (or cyclic) imports
    # payment = models.OneToOneField(to='funds.Payment', on_delete=models.RESTRICT, null=True, blank=True)

    # unique code Ex: GFM107
    ref_code = models.CharField(max_length=200, null=True, blank=True)
    tds = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    magic_bonus = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)




    # create Timestamp automatically
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # to get right name in admin panel
    class Meta:
        verbose_name = 'discountbonus'
        verbose_name_plural = 'discountbonuses'

    # def __str__(self):
    #     return self.account

# class LeadershipBonus(models.Model):
#     # rank from 0 to 7
#     rank = models.IntegerField(default=0)
#     # name of rank
#     level = models.CharField(max_length=200, unique=True)
#     # incentive can be used in percentage as per level
#     incentive = models.IntegerField(default=0)
#     # check referral chart for details of used_upto
#     used_upto = models.IntegerField(default=0, null=True, blank=True)

#     # create Timestamp automatically
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

#     class Meta:
#         verbose_name = 'leadershipbonus'
#         verbose_name_plural = 'leadershipbonuses'

#     def __str__(self):
#         return self.level

class DirectBonus(models.Model):
    # OneToOne relatioship
    # To delete it you will have to delete all objects that reference it manually. RESTRICT
    # to='funds.Payment' used to avoid Circular (or cyclic) imports
    # payment = models.OneToOneField(to='funds.Payment', on_delete=models.RESTRICT)
    # one to many with Account, on_delete it will remain
    # referral = models.ForeignKey(Referral, null=True, blank=True, on_delete=models.SET_NULL)
    account = models.OneToOneField(Account, on_delete=models.RESTRICT, null=True, blank=True)
    ref_code = models.CharField(max_length=200, null=True, blank=True)
    tds = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    magic_bonus = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    # create Timestamp automatically
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # to get right name in admin panel
    class Meta:
        verbose_name = 'directbonus'
        verbose_name_plural = 'directbonuses'

    def __str__(self):
        return self.ref_code


# class MagicBonus(models.Model):
#     # OneToOne relatioship
#     # To delete it you will have to delete all objects that reference it manually. RESTRICT
#     directbonus = models.OneToOneField(DirectBonus, on_delete=models.RESTRICT, null=True, blank=True)

#     discountbonus = models.OneToOneField(DiscountBonus, on_delete=models.RESTRICT, null=True, blank=True)

#     amount = models.DecimalField(max_digits=9, decimal_places=2)

#     # create Timestamp automatically
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

#     class Meta:
#         verbose_name = 'magicbonus'
#         verbose_name_plural = 'magicbonuses'

#     # def __str__(self):
#     #     return self.directbonus.ref_num