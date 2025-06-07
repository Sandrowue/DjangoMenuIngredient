import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=75)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=15)
    unit_price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    def calculate_total_price(self):
        return self.quantity * self.unit_price


class MenuItem(models.Model):
    title = models.CharField(max_length=75)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.title

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField("date purchased")

    def was_purchased_recently(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1)

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)