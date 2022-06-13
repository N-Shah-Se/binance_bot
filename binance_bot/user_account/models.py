from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
import datetime
from django.contrib.auth import get_user_model
import jwt
from datetime import datetime, timedelta

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class UserAccountManager(BaseUserManager):
    def create_user(self, email,phone,invitation_code, password=None, is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            invitation_code=invitation_code,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, username, password):
    #     import pdb;
    #     pdb.set_trace()
    #     user = self.create_user(
    #         email=self.normalize_email(email),
    #         password=password,
    #         username=username,
    #     )
    #     user.is_admin = True
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, phone, password, invitation_code=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone=phone,
            invitation_code="GFM2002"
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class Profile(AbstractBaseUser,PermissionsMixin):
    password = models.CharField(max_length=150)
    phone = models.CharField(max_length=17,validators=[phone_regex],unique=True)
    email = models.EmailField(max_length=100,unique=True)
    invitation_code = models.CharField(max_length=20)
    account_created = models.DateTimeField(default=datetime.now())
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null= True,default=None)
    last_name = models.CharField(max_length=100, null=True,default=None)
    image_url = models.ImageField(upload_to='images/',max_length=200,default=None)
    username = models.CharField(max_length=200, null=True,default=None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserAccountManager()
    # uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        # dt = datetime.now() + timedelta(hours=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': datetime.now()+ timedelta(minutes=45)
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
