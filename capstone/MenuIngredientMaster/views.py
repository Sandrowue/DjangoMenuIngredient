from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Ingredient, MenuItem, RecipeRequirements
from .forms import RecipeEditForm

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
    if request.method == "POST":
        print('Meni läpi')
        newIngredient = Ingredient()
        newIngredient.name = request.POST['ingredientInput'] 
        newIngredient.quantity = int(request.POST['amountInput'])
        newIngredient.unit = request.POST['unitInput']
        newIngredient.unit_price = float(request.POST['unitPriceInput'])
        newIngredient.total_price = newIngredient.calculate_total_price()
        newIngredient.save()

    return render(request, "MenuIngredientMaster/addIngredient.html")

def changeIngredient(request, ingredient_id):
    ingredientitem = get_object_or_404(Ingredient, id=ingredient_id)
    if request.method == 'POST':
        ingredient = ingredientitem
        ingredient.name = request.POST['ingredientInput'] 
        ingredient.quantity = int(request.POST['amountInput'])
        ingredient.unit = request.POST['unitInput']
        ingredient.unit_price = float(request.POST['unitPriceInput'])
        ingredient.total_price = ingredient.calculate_total_price()
        ingredient.save()
    return render(request, "MenuIngredientMaster/changeIngredient.html", {"ingredientitem": ingredientitem})


def deleteIngredient(request, ingredient_id):
    toDelete = Ingredient.objects.get(id=ingredient_id)
    toDelete.delete()
    return redirect("ingredients")
    

# Using render instead of HttpResponse
def aviableMenus(request):
    allMenus = MenuItem.objects.order_by("title")
    context = {
        "allMenus": allMenus,
    }
    return render(request, "MenuIngredientMaster/menus.html", context)

def addMenu(request):
    if request.method == "POST":
        newMenu = MenuItem()
        newMenu.title = request.POST['menuInput']
        newMenu.price = request.POST['priceInput']
        newMenu.save()

    return render(request, 'MenuIngredientMaster/addMenu.html')

def changeMenu(request, menuitem_id):
    menuitem = get_object_or_404(MenuItem, id=menuitem_id)
    if request.method == "POST":
        menu = menuitem
        menu.title = request.POST['menuInput']
        menu.price = request.POST['priceInput']
        menu.save()
    return render(request, 'MenuIngredientMaster/changeMenu.html', {"menuitem": menuitem})

def deleteMenu(request, menuitem_id):
    toDelete = MenuItem.objects.get(id=menuitem_id)
    toDelete.delete()
    return redirect("aviableMenus")

def showReceipe(request, menuitem_id):
    ingredients = Ingredient.objects.all()
    receipe = RecipeRequirements.objects.filter(menu_item_id=menuitem_id)
    return render(request, 'MenuIngredientMaster/showReceipe.html', {"receipe": receipe, "ingredients": ingredients})

def addRecipeItem(request):
    if request.method == "POST":
        form = RecipeEditForm(request.POST) 
        if form.is_valid():
            newItem = RecipeRequirements()
            newItem.menu_item = form.cleaned_data["menu_item"]
            newItem.ingredient = form.cleaned_data["ingredient"]
            newItem.quantity = float(form.cleaned_data["quantity"])
            newItem.save()
            return redirect('addRecipeItem')
    else:
        form = RecipeEditForm()
    ingredients = Ingredient.objects.all()
    return render(request, 'MenuIngredientMaster/addRecipeItem.html' , {"form":form, "ingredients": ingredients})

def financials(request):
    return HttpResponse("Django Delight's profit and revenue.")

def sold(request):
    return HttpResponse("Recently sold Menus:")