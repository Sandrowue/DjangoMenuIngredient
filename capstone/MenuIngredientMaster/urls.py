from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("ingredients", views.ingredients, name="ingredients"),
    path("addIngredient", views.addIngredient, name="addIngredient"),
    path("changeIngredient/<int:ingredient_id>", views.changeIngredient, name="changeIngredient"),
    path("deleteIngredient/<int:ingredient_id>", views.deleteIngredient, name="deleteIngredient"),
    path("changeAcquiredIngredient/<int:acquiredingredient_id>", views.changeAcquiredIngredient, name="changeAcquiredIngredient"),
    path("deleteAcquiredIngredient/<int:acquiredingredient_id>", views.deleteAcquiredIngredient, name="deleteAcquiredIngredient"),
    path("aviableMenus", views.aviableMenus, name="aviableMenus"),
    path("addMenu", views.addMenu, name="addMenu"),
    path("changeMenu/<int:menuitem_id>", views.changeMenu, name="changeMenu"),
    path("deleteMenu/<int:menuitem_id>", views.deleteMenu, name="deleteMenu"),
    path("showRecipe/<int:menuitem_id>", views.showRecipe, name="showRecipe"),
    path("addRecipeItem", views.addRecipeItem, name="addRecipeItem"),
    path("changeRecipeItem/<int:reciperequirements_id>", views.changeRecipeItem, name="changeRecipeItem"),
    path("deleteRecipeItem/<int:reciperequirements_id>", views.deleteRecipeItem, name="deleteRecipeItem"),
    path("addSoldEvent", views.addSoldEvent, name="addSoldEvent"),
    path("deleteSoldEvent/<int:purchase_id>", views.deleteSoldEvent, name="deleteSoldEvent"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]