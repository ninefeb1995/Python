from django.db import models
from django.utils import timezone


class RawData(models.Model):
    co = models.FloatField()
    oxi = models.FloatField()
    measuring_date = models.DateTimeField(auto_created=True)
    node = models.ForeignKey('manage_devices.Node', on_delete=models.SET_NULL, null=True)
    node_name = models.CharField(max_length=255)  # This field is to ensure data belonged
    # to what when node has been deleted

    class Meta:
        get_latest_by = "measuring_date"


class Data(models.Model):
    co = models.FloatField()
    oxi = models.FloatField()
    measuring_date = models.DateField(default=timezone.now())
    area = models.ForeignKey('Area', on_delete=models.CASCADE)


class Area(models.Model):
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name

