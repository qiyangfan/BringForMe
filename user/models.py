from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=15)
    address = models.BigIntegerField(null=True, blank=True)
    balance = models.FloatField(default=0)
