from django.contrib import admin

# Register your models here.
from .models import Ingredient, MenuItem, Purchase, RecipeRequirements

admin.site.register(Ingredient)
admin.site.register(MenuItem)
admin.site.register(Purchase)
admin.site.register(RecipeRequirements)
