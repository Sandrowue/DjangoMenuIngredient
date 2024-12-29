from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Welcome to Django Delight's kitchen!")

def ingredients(request):
    return HttpResponse("All ingredients in the inventory:")

def deleteIngredient(request, deleteIngredient=None):
    return HttpResponse("You're about to delete the ingredient %s." % deleteIngredient)

def aviableMenus(request):
    return HttpResponse("The menus and drinks we serve:")

def itemsInMenu(request, menu_item=None):
    response = "This menu has following ingredients: %s."
    return HttpResponse(response % menu_item)

def financials(request):
    return HttpResponse("Django Delight's profit and revenue.")

def sold(request):
    return HttpResponse("Recently sold Menus:")