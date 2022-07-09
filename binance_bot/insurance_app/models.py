from django.db import models

# Create your models here
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from datetime import datetime, timedelta

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Insurance(models.Model):
    title = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    dob = models.DateTimeField(default=False)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=15,validators=[phone_regex],unique=True)
    occupation = models.CharField(max_length=100)
    house_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=30)
    aadhar_card_no = models.CharField(max_length=100)
    pan_card_no = models.CharField(max_length=100)
    gstn_no = models.CharField(max_length=100, null= True,default=None)

    nominee_name = models.CharField(max_length=100)
    nominee_age = models.CharField(max_length=100)
    nominee_relation = models.CharField(max_length=100)
    aadhar_no = models.CharField(max_length=100)
    aadhar_pan = models.CharField(max_length=30)

    self_data = models.CharField(max_length=100, null=True,default=None)
    death = models.CharField(max_length=200, null=True,default=None)
    permanent_total_disable = models.CharField(max_length=100)
    permanent_partial_disable = models.CharField(max_length=100,null=True)
    temporary_total_disable = models.CharField(max_length=100,null=True)
    login_email=models.EmailField(max_length=100,null=True,default=None)

    def __str__(self):
        return self.cnic
