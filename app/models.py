from django.db import models


class Ship(models.Model):
    imo = models.IntegerField()
    name = models.CharField(max_length=17)


class Position(models.Model):
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=19)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
