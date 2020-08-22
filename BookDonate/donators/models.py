from django.db import models


# Create your models here.
class Book(models.Model):
    LANGUAGE_CHOICES = [('CN', 'Chinese'), ('EN', 'ENGLISH')]
    name = models.CharField(max_length=100)
    donator = models.CharField(max_length=100)
    author = models.CharField(max_length=30)
    category = models.CharField(max_length=30, blank=True)
    description = models.TextField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    donate_date = models.DateTimeField()
    rate = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    prices = models.ManyToManyField('Price', blank=True)


class Price(models.Model):
    name = models.CharField(max_length=50)