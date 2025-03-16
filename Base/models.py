from django.db import models

# Create your models here.

class Sensor_Reading(models.Model):
    sensor = models.ForeignKey('Sensor_ID', null=True, related_name="readings", on_delete=models.CASCADE)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    lux = models.FloatField(null=True)

class Sensor_ID(models.Model):
    sensor_id = models.CharField(default=0, max_length=128)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
