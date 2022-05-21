from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from django.contrib.auth import get_user_model

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_admin(self, email, username, password):
    #     user = self.create_user(
    #         email=self.normalize_email(email),
    #         password=password,
    #         username=username,
    #     )
    #     user.is_admin = True
        # user.is_staff = True
        # user.is_superuser = True
        # user.save(using=self._db)
        # return user




class Profile(AbstractBaseUser):
    password = models.CharField(max_length=150)
    phone = models.CharField(max_length=17,validators=[phone_regex],unique=True)
    email = models.EmailField(max_length=100,unique=True)
    invitation_code = models.CharField(max_length=20)
    account_created = models.DateTimeField(default=datetime.datetime.now())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserAccountManager()
    # uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    def __str__(self):
        return self.email