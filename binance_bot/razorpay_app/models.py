from django.db import models

class razorpay_account(models.Model):

    razorpay_payment_id = models.CharField(max_length=150)
    razorpay_order_id = models.CharField(max_length=150)
    razorpay_signature = models.CharField(max_length=150)

    def __str__(self):
        return self.id
