from django.db import models


# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=15)
    balance = models.FloatField(default=0)


class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=15)
    province = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    remark = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    is_default = models.BooleanField(default=False)
