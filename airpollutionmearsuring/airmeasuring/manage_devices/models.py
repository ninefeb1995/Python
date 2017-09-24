from django.db import models
from django.utils import timezone


class Node(models.Model):
    name = models.CharField(max_length=255)
    area = models.ForeignKey('dashboard.Area', on_delete=models.CASCADE)
    node_identification = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    gateway_id = models.ForeignKey('Node', blank=True, null=True)
    is_available = models.BooleanField(default=False)
    longitude = models.CharField(max_length=255, null=True)
    latitude = models.CharField(max_length=255, null=True)
    last_connect = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name


