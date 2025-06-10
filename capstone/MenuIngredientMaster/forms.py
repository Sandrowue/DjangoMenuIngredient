from django import forms
from .models import RecipeRequirements, Ingredient, MenuItem

class RecipeEditForm(forms.Form):
    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.order_by("title"), label="Menu")
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.order_by("name"), label="Ingredient")
    quantity = forms.FloatField(label="Amount")
    cost = forms.FloatField(label="Price")

    
    