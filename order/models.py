from django.db import models

from user.models import User, Address


# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination = models.JSONField()
    description = models.TextField()
    commission = models.FloatField(null=True, blank=True, default=0)
    status = models.SmallIntegerField(choices=(
        (0, 'Awaiting Acceptance'),
        (1, 'Order Accepted'),
        (2, 'Completed'),
        (3, 'Cancelled')
    ), default=0)
    acceptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acceptor', null=True, blank=True)
    images = models.JSONField(null=True, blank=True)
