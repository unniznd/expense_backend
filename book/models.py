from django.db import models

class Book(models.Model):
    bookNumber = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pageLeft = models.IntegerField()
    isReturned = models.BooleanField(default=False)
    lastUpdated = models.DateTimeField(auto_now=True)