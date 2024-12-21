from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=75)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=15)
    unit_price = models.FloatField(default=0)

class MenuItem(models.Model):
    title = models.CharField(max_length=75)
    price = models.FloatField(default=0)

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField("date purchased")

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)