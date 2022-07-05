from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
import datetime
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

class Order(models.Model):
    email = models.EmailField(max_length=100,unique=True)
    symbol= models.CharField(max_length=150),
    orderId= models.CharField(max_length=150),
    clientOrderId= models.CharField(max_length=150),
    transactTime= models.CharField(max_length=150),
    price = models.CharField(max_length=150),
    origQty = models.CharField(max_length=150),
    executedQty =  models.CharField(max_length=150),
    cummulativeQuoteQty = models.CharField(max_length=150),
    status = models.CharField(max_length=150),
    timeInForce = models.CharField(max_length=150),
    type=models.CharField(max_length=150),
    side = models.CharField(max_length=150)

    # uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    def __str__(self):
        return self.id