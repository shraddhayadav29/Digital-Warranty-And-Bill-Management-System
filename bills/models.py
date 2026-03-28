from django.db import models
from django.contrib.auth.models import User

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    bill_image = models.ImageField(upload_to='bills/', null=True, blank=True)
    email_sent = models.BooleanField(default=False)
    extended_months = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name

