from django.db import models
from django.contrib.auth.models import User
import uuid

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    avatar = models.ImageField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default = 10.55)
    image = models.ImageField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


4