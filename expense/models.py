from django.db import models

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    byWhom = models.CharField(max_length=100)
    lastUpdated = models.DateTimeField(auto_now=True)
