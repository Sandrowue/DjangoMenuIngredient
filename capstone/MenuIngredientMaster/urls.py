from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ingredients", views.ingredients, name="ingredients"),
    path("addIngredient", views.addIngredient, name="addIngredient"),
    path("changeIngredient/<int:ingredient_id>", views.changeIngredient, name="changeIngredient"),
    path("deleteIngredient/<int:ingredient_id>", views.deleteIngredient, name="deleteIngredient"),
    path("aviableMenus", views.aviableMenus, name="aviableMenus"),
    path("addMenu", views.addMenu, name="addMenu"),
    path("changeMenu/<int:menuitem_id>", views.changeMenu, name="changeMenu"),
    path("deleteMenu/<int:menuitem_id>", views.deleteMenu, name="deleteMenu"),
    path("showReceipe/<int:menuitem_id>", views.showReceipe, name="showReceipe"),
    path("financials", views.financials, name="financials"),
    path("sold", views.sold, name="sold"),
    path("addRecipeItem", views.addRecipeItem, name="addRecipeItem"),
]