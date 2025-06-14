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
        return redirect("addIngredient")

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

def addMenu(request):
    if request.method == "POST":
        newMenu = MenuItem()
        newMenu.title = request.POST['menuInput']
        newMenu.price = request.POST['priceInput']
        newMenu.save()
    return render(request, 'MenuIngredientMaster/addMenu.html')

# Using get_object_or_404 
def itemsInMenu(request, menu_item=None):
    specificMenu = get_object_or_404(RecipeRequirements, pk=menu_item)
    return HttpResponse("This menu has following ingredients: %s." % menu_item, {"specificMenu": specificMenu})

def addRecipeItem(request):
    if request.method == "POST":
        form = RecipeEditForm(request.POST) 
        if form.is_valid():
            newItem = RecipeRequirements()
            newItem.menu_item = form.cleaned_data["menu_item"]
            newItem.ingredient = form.cleaned_data["ingredient"]
            newItem.quantity = float(form.cleaned_data["quantity"])
            newItem.cost = float(form.cleaned_data["cost"])
            newItem.save()
            return redirect('addRecipeItem')
    else:
        form = RecipeEditForm()
    return render(request, 'MenuIngredientMaster/addRecipeItem.html' , {"form":form})


def financials(request):
    return HttpResponse("Django Delight's profit and revenue.")

def sold(request):
    return HttpResponse("Recently sold Menus:")