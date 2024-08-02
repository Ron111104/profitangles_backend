# stocks/models.py
from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    price = models.FloatField()
    prev_close=models.FloatField()
    sector = models.CharField(max_length=50, null=True, blank=True)
    index = models.CharField(max_length=50, null=True, blank=True)
