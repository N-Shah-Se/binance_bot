from django.db import models
import datetime

class Order(models.Model):
    email = models.EmailField(max_length=100,null=True,default=None)
    symbol= models.CharField(max_length=150,null=True,default=None)
    orderId= models.CharField(max_length=150,null=True,default=None)
    clientOrderId= models.CharField(max_length=150,null=True,default=None)
    transactTime= models.DateTimeField()
    price = models.CharField(max_length=150,null=True,default=None)
    origQty = models.CharField(max_length=150,null=True,default=None)
    executedQty =  models.CharField(max_length=150,null=True,default=None)
    cummulativeQuoteQty = models.CharField(max_length=150,null=True,default=None)
    status = models.CharField(max_length=150,null=True,default=None)
    timeInForce = models.CharField(max_length=150,null=True,default=None)
    type=models.CharField(max_length=150,null=True,default=None)
    side = models.CharField(max_length=150,null=True,default=None)
    profit = models.CharField(max_length=150,null=True,default='0')

    # uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    def __str__(self):
        return self.id