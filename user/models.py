from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=4)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=20)
    avatar = models.ImageField(null=True, blank=True)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=63)
    province = models.CharField(max_length=31, null=True, blank=True)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    remark = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=10)
    contact_person = models.CharField(max_length=255)
    country_code = models.CharField(max_length=3)
    phone = models.CharField(max_length=12)
    is_default = models.BooleanField(default=False)
