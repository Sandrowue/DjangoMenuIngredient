from django import forms
from .models import Ingredient, MenuItem, Purchase

class RecipeEditForm(forms.Form):
    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.order_by("title"), label="Menu")
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.order_by("name"), label="Ingredient")
    quantity = forms.FloatField(label="Amount")

class SoldEditForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields= ['menu_item', 'timestamp']
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    

    
    