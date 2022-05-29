from django.db import models
from user_account.models import Profile
# Create your models here.

class BotUser(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
	api_key = models.CharField(max_length=200, null=False, blank=False)
	secret_key = models.CharField(max_length=200, null=False, blank=False)
