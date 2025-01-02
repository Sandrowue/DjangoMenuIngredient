from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Ingredient, MenuItem

# Create your views here.
def index(request):
    return HttpResponse("Welcome to Django Delight's kitchen!")

def ingredients(request):
    allIngredients = Ingredient.objects.order_by("name")
    template = loader.get_template("MenuIngredientMaster/ingredients.html")
    context = {
        "allIngredients": allIngredients,
    }
    return HttpResponse(template.render(context, request))

def deleteIngredient(request, deleteIngredient=None):
    return HttpResponse("You're about to delete the ingredient %s." % deleteIngredient)

def aviableMenus(request):
    allMenus = MenuItem.objects.order_by("title")
    template = loader.get_template("MenuIngredientMaster/menus.html")
    context = {
        "allMenus": allMenus,
    }
    return HttpResponse(template.render(context, request))

def itemsInMenu(request, menu_item=None):
    response = "This menu has following ingredients: %s."
    return HttpResponse(response % menu_item)

def financials(request):
    return HttpResponse("Django Delight's profit and revenue.")

def sold(request):
    return HttpResponse("Recently sold Menus:")