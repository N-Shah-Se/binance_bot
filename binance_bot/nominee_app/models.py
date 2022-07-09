from django.db import models

# Create your models here


class Nominee(models.Model):
    nominee_name = models.CharField(max_length=100)
    nominee_age = models.CharField(max_length=100)
    nominee_relation = models.CharField(max_length=100)
    aadhar_no = models.CharField(max_length=100)
    aadhar_pan = models.CharField(max_length=30)
    account_number = models.CharField(max_length=100, null=True,default=None)
    account_holder = models.CharField(max_length=200, null=True,default=None)
    ifsc_code = models.CharField(max_length=100)
    rbi_bank = models.CharField(max_length=100,null=True)
    login_email=models.EmailField(max_length=100,null=True,default=None)

    def __str__(self):
        return self.nominee_name
