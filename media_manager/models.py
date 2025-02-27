from django.db import models

# Create your models here.
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField()

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.FileField()