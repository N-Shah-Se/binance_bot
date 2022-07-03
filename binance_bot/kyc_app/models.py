from django.db import models

# Create your models here
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from datetime import datetime, timedelta
from .constants import KYCStatus

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class KYC(models.Model):
    title = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    fname = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    dob = models.DateTimeField(default=False)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=15,validators=[phone_regex],unique=True)
    house_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=30)
    cnic = models.CharField(max_length=100)
    cnic_front = models.ImageField(upload_to='front/',max_length=200,default=None)
    cnic_back = models.ImageField(upload_to='back/',max_length=200,default=None)
    card_no = models.CharField(max_length=100)
    card_image = models.ImageField(upload_to='bank/',max_length=200,default=None)
    account_no = models.CharField(max_length=100, null= True,default=None)
    account_holder = models.CharField(max_length=100, null=True,default=None)
    ifsc_code = models.CharField(max_length=200, null=True,default=None)
    bank_name = models.CharField(max_length=100)
    kyc_status = models.CharField(max_length=100,default="PENDING")
    login_email=models.EmailField(max_length=100,null=True,default=None)

    def __str__(self):
        return self.cnic
