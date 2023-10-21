from django.db import models
from django.contrib.auth.models import User


class ProductItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity_in_stock = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


