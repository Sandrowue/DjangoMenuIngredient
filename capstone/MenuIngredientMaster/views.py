from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import loader

from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Ingredient, MenuItem, RecipeRequirements, Purchase, AcquiredIngredient
from .forms import RecipeEditForm, SoldEditForm
from datetime import datetime

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

# Create your views here.
def index(request):
    allIngredients = Ingredient.objects.order_by("name")
    allMenus = MenuItem.objects.order_by("title")
    start = request.GET.get("timespan_start")
    menuStart = request.GET.get("menu_timespan_start")
    end = request.GET.get('timespan_end')
    menuEnd = request.GET.get("menu_timespan_end")
    ingredient_names = request.GET.getlist("ingredient_names")
    menu_names = request.GET.getlist("menu_names")
    ingredient_total_cost = 0
    income = 0
    if start or end or ingredient_names:
        purchaseEvents = AcquiredIngredient.objects.order_by("-timestamp")
        if start:
            start_dt = datetime.strptime(start, "%Y-%m-%dT%H:%M")
            if start_dt:
                purchaseEvents = purchaseEvents.filter(timestamp__gte=start_dt)
        if end:
            end_dt = datetime.strptime(end, "%Y-%m-%dT%H:%M")
            if end_dt:
                purchaseEvents = purchaseEvents.filter(timestamp__lte=end_dt)
        if ingredient_names and "__all__" not in ingredient_names:
            purchaseEvents = purchaseEvents.filter(name__in=ingredient_names)
        ingredient_total_cost = sum(p.total_price for p in purchaseEvents)
    else:
        purchaseEvents = AcquiredIngredient.objects.none()

    if menuStart or menuEnd or menu_names:        
        soldMenus = Purchase.objects.order_by("-timestamp")
        if menuStart:
            menuStart_dt = datetime.strptime(menuStart, "%Y-%m-%dT%H:%M")
            if menuStart_dt:
                soldMenus = soldMenus.filter(timestamp__gte=menuStart_dt)
        if menuEnd:
            menuEnd_dt = datetime.strptime(menuEnd, "%Y-%m-%dT%H:%M")
            if menuEnd_dt:
                soldMenus = soldMenus.filter(timestamp__lte=menuEnd_dt)
        if menu_names and "__all__" not in menu_names:
            soldMenus = soldMenus.filter(menu_item__title__in=menu_names)
        income = sum(p.price for p in soldMenus)
    else:
        soldMenus = Purchase.objects.none()

    balance = income - ingredient_total_cost

    context = {
        "purchaseEvents": purchaseEvents,
        "allIngredients": allIngredients,
        "selected_ingredient_names": ingredient_names,
        "allMenus": allMenus,
        "soldMenus": soldMenus,
        "selected_menu_names": menu_names,
        "ingredient_total_cost": ingredient_total_cost,
        "income": income,
        "balance": balance
    }
    return render(request, "MenuIngredientMaster/index.html", context)


def ingredients(request):
    allIngredients = Ingredient.objects.order_by("name")
    template = loader.get_template("MenuIngredientMaster/ingredients.html")
    context = {
        "allIngredients": allIngredients,   
    }
    return HttpResponse(template.render(context, request))

@login_required
def addIngredient(request):
    if request.method == "POST":
        name = request.POST['ingredientInput']
        amount = int(request.POST['amountInput'])
        unit = request.POST['unitInput']
        unit_price = float(request.POST['unitPriceInput'])

        newAcquiredIngredient = AcquiredIngredient()
        newAcquiredIngredient.timestamp = request.POST['timestampInput']
        newAcquiredIngredient.name = request.POST['ingredientInput']
        newAcquiredIngredient.quantity = float(request.POST['amountInput'])
        newAcquiredIngredient.unit = request.POST['unitInput']
        newAcquiredIngredient.unit_price = float(request.POST['unitPriceInput'])
        newAcquiredIngredient.total_price = newAcquiredIngredient.calculate_total_price()
        newAcquiredIngredient.save()
        

        try: 
            existing = Ingredient.objects.get(name=name, unit=unit)
            new_quantity = existing.quantity + amount
            new_untit_price = ((existing.unit_price * existing.quantity) + (unit_price * amount)) / new_quantity
            existing.quantity = new_quantity
            existing.unit_price = new_untit_price
            existing.total_price = existing.calculate_total_price()
            existing.save()

        except Ingredient.DoesNotExist:
            newIngredient = Ingredient()
            newIngredient.name = request.POST['ingredientInput'] 
            newIngredient.quantity = float(request.POST['amountInput'])
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
        ingredient.quantity = float(request.POST['amountInput'])
        ingredient.unit = request.POST['unitInput']
        ingredient.unit_price = float(request.POST['unitPriceInput'])
        ingredient.total_price = ingredient.calculate_total_price()
        ingredient.save()
    return render(request, "MenuIngredientMaster/changeIngredient.html", {"ingredientitem": ingredientitem})

def changeAcquiredIngredient(request, acquiredingredient_id):
    ingredientitem = get_object_or_404(AcquiredIngredient, id=acquiredingredient_id)
    if request.method == 'POST':
        ingredient = ingredientitem
        ingredient.name = request.POST['ingredientInput'] 
        ingredient.quantity = float(request.POST['amountInput'])
        ingredient.unit = request.POST['unitInput']
        ingredient.unit_price = float(request.POST['unitPriceInput'])
        ingredient.total_price = ingredient.calculate_total_price()
        ingredient.timestamp = request.POST['timestampInput']
        ingredient.save()
    return render(request, "MenuIngredientMaster/changeAcquiredIngredient.html", {"ingredientitem": ingredientitem})

@admin_required
def deleteIngredient(request, ingredient_id):
    toDelete = Ingredient.objects.get(id=ingredient_id)
    toDelete.delete()
    return redirect("ingredients")

@admin_required
def deleteAcquiredIngredient(request, acquiredingredient_id):
    toDelete = AcquiredIngredient.objects.get(id=acquiredingredient_id)
    toDelete.delete()
    return redirect("ingredients")
    

# Using render instead of HttpResponse
def aviableMenus(request):
    allMenus = MenuItem.objects.order_by("title")
    soldMenus = Purchase.objects.order_by("-timestamp")
    context = {
        "allMenus": allMenus,
        "soldMenus": soldMenus,
    }
    return render(request, "MenuIngredientMaster/menus.html", context)

@admin_required
def addMenu(request):
    if request.method == "POST":
        newMenu = MenuItem()
        newMenu.title = request.POST['menuInput']
        newMenu.price = request.POST['priceInput']
        newMenu.save()

    return render(request, 'MenuIngredientMaster/addMenu.html')

@admin_required
def changeMenu(request, menuitem_id):
    menuitem = get_object_or_404(MenuItem, id=menuitem_id)
    if request.method == "POST":
        menu = menuitem
        menu.title = request.POST['menuInput']
        menu.price = request.POST['priceInput']
        menu.save()
    return render(request, 'MenuIngredientMaster/changeMenu.html', {"menuitem": menuitem})

@admin_required
def deleteMenu(request, menuitem_id):
    toDelete = MenuItem.objects.get(id=menuitem_id)
    toDelete.delete()
    return redirect("aviableMenus")

def showRecipe(request, menuitem_id):
    menu= get_object_or_404(MenuItem, id=menuitem_id)
    receipe = RecipeRequirements.objects.filter(menu_item_id=menuitem_id).order_by('ingredient__name')
    total_cost = sum(item.cost for item in receipe)
    return render(request, 'MenuIngredientMaster/showRecipe.html', {"receipe": receipe, "menu": menu, "total_cost": total_cost})

@admin_required
def addRecipeItem(request):
    menu_item_id = request.GET.get("menu_item")
    if request.method == "POST":
        form = RecipeEditForm(request.POST) 
        if form.is_valid():
            newItem = RecipeRequirements()
            newItem.menu_item = form.cleaned_data["menu_item"]
            newItem.ingredient = form.cleaned_data["ingredient"]
            newItem.quantity = float(form.cleaned_data["quantity"])
            newItem.cost = float(newItem.ingredient.unit_price * newItem.quantity)
            newItem.save()
            return redirect(f'{request.path}?menu_item={newItem.menu_item.id}')
    else: 
        if menu_item_id:
            form = RecipeEditForm(initial={"menu_item": menu_item_id})
        else:
            form = RecipeEditForm()
    ingredients = Ingredient.objects.all()
    return render(request, 'MenuIngredientMaster/addRecipeItem.html' , {"form":form, "ingredients": ingredients, "menu_item_id": menu_item_id})

@admin_required
def changeRecipeItem(request, reciperequirements_id):
    recipe_item = get_object_or_404(RecipeRequirements, id=reciperequirements_id)
    if request.method == "POST":
        form = RecipeEditForm(request.POST) 
        if form.is_valid():
            recipe_item.menu_item = form.cleaned_data["menu_item"]
            recipe_item.ingredient = form.cleaned_data["ingredient"]
            recipe_item.quantity = float(form.cleaned_data["quantity"])
            recipe_item.cost = float(recipe_item.ingredient.unit_price * recipe_item.quantity)
            recipe_item.save()
            return redirect('showRecipe', menuitem_id=recipe_item.menu_item.id)
    else:
        form = RecipeEditForm(initial={
            "menu_item": recipe_item.menu_item,
            "ingredient": recipe_item.ingredient,
            "quantity": recipe_item.quantity,
        })
    ingredients = Ingredient.objects.all()
    return render(request, 'MenuIngredientMaster/changeRecipeItem.html' , {"form":form, "ingredients": ingredients, "menu": recipe_item.menu_item})

@admin_required
def deleteRecipeItem(request, reciperequirements_id):
    toDelete = get_object_or_404(RecipeRequirements, id=reciperequirements_id)
    menuitem_id = toDelete.menu_item.id
    toDelete.delete()
    return redirect("showRecipe", menuitem_id=menuitem_id)

@login_required
def addSoldEvent(request):
    if request.method == "POST":
        form = SoldEditForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.price = purchase.menu_item.price
            purchase.save()

            purchasedMenu = MenuItem.objects.get(id=purchase.menu_item_id)
            menuIngredients = RecipeRequirements.objects.filter(menu_item=purchasedMenu)
            for item in menuIngredients:
                menuItem = Ingredient.objects.get(name=item.ingredient)
                substract = menuItem.quantity - item.quantity
                menuItem.quantity = substract
                menuItem.total_price = menuItem.calculate_total_price()
                menuItem.save()

            return redirect('index')
        
    else:
        form = SoldEditForm()
    form.fields['menu_item'].queryset = MenuItem.objects.order_by('title')
    return render(request, "MenuIngredientMaster/addSoldEvent.html", {"form": form})

@admin_required
def deleteSoldEvent(request, purchase_id):
    toDelete = Purchase.objects.get(id=purchase_id)
    toDelete.delete()
    return redirect("aviableMenus")

def account(request):
    pass
        