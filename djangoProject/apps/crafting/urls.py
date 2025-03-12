from django.urls import path
from apps.crafting.views import recipe_list, recipe_detail, craft_item

urlpatterns = [
    path("recipes/", recipe_list, name="recipe_list"),
    path("recipes/<int:recipe_id>/", recipe_detail, name="recipe_detail"),
    path("craft/<int:recipe_id>/", craft_item, name="craft_item"),
]