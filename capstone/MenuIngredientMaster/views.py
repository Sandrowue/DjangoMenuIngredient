from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Ingredient, MenuItem, RecipeRequirement

# Create your views here.
def index(request):
    return render(request, "MenuIngredientMaster/index.html")

def ingredients(request):
    allIngredients = Ingredient.objects.order_by("name")
    template = loader.get_template("MenuIngredientMaster/ingredients.html")
    context = {
        "allIngredients": allIngredients,
    }
    return HttpResponse(template.render(context, request))

def addIngredient(request):
    print(request.method)
    if request.method == "POST":
        print('Meni läpi')
        newIngredient = Ingredient()
        newIngredient.name = request.POST['ingredientInput'] 
        newIngredient.quantity = int(request.POST['amountInput'])
        newIngredient.unit = request.POST['unitInput']
        newIngredient.unit_price = int(request.POST['unitPriceInput'])
        newIngredient.save()
    return render(request, "MenuIngredientMaster/addIngredient.html")

def deleteIngredient(request, deleteIngredient=None):
    try:
        toDelete = Ingredient.objects.get(pk=deleteIngredient)
    except Ingredient.DoesNotExist:
        raise Http404("Questien does not exist!")
    return HttpResponse("You're about to delete the ingredient %s." % deleteIngredient, {"toDelete": toDelete})

# Using render instead of HttpResponse
def aviableMenus(request):
    allMenus = MenuItem.objects.order_by("title")
    context = {
        "allMenus": allMenus,
    }
    return render(request, "MenuIngredientMaster/menus.html", context)

# Using get_object_or_404 
def itemsInMenu(request, menu_item=None):
    specificMenu = get_object_or_404(RecipeRequirement, pk=menu_item)
    return HttpResponse("This menu has following ingredients: %s." % menu_item, {"specificMenu": specificMenu})

def financials(request):
    return HttpResponse("Django Delight's profit and revenue.")

def sold(request):
    return HttpResponse("Recently sold Menus:")