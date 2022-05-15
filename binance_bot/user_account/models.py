from django.db import models
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Profile(models.Model):
    password = models.CharField(max_length=150)
    phone = models.CharField(max_length=17,validators=[phone_regex],unique=True)
    email = models.EmailField(max_length=100,unique=True)
    invitation_code = models.CharField(max_length=20)
    # uuid = models.UUIDField(default=uuid.uuid4,editable=False)