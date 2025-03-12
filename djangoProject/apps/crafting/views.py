import random
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from apps.crafting.models import Recipe, RecipeIngredient
from apps.crates.models import InventoryItem, Item
from apps.users.models import UserProfile


@login_required
def recipe_list(request):
    """Display all available recipes."""
    recipes = Recipe.objects.all()
    return render(request, "crafting/recipe_list.html", {"recipes": recipes})


@login_required
def recipe_detail(request, recipe_id):
    """Display details of a specific recipe including user's inventory counts for each ingredient."""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    # Build a dictionary mapping ingredient ID (as string) to quantity in user's inventory
    inventory_info = {}
    for ri in ingredients:
        inv_item = InventoryItem.objects.filter(user=request.user, item=ri.ingredient).first()
        # Convert key to string for easier lookup in templates.
        inventory_info[str(ri.ingredient.id)] = inv_item.quantity if inv_item else 0

    return render(request, "crafting/recipe_detail.html", {
        "recipe": recipe,
        "ingredients": ingredients,
        "inventory_info": inventory_info
    })

@login_required
def craft_item(request, recipe_id):
    """
    Process a crafting request.
    Checks if the user has sufficient ingredients; if yes, consumes them
    and adds the crafted item to the inventory.
    Returns JSON with success status and message.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    missing = []
    for ingredient in ingredients:
        inv_item = InventoryItem.objects.filter(user=request.user, item=ingredient.ingredient).first()
        if not inv_item or inv_item.quantity < ingredient.quantity:
            missing.append(f"{ingredient.ingredient.name} (need {ingredient.quantity})")

    if missing:
        return JsonResponse({"error": "Insufficient ingredients: " + ", ".join(missing)}, status=400)

    try:
        with transaction.atomic():
            # Consume the required ingredients
            for ingredient in ingredients:
                inv_item = InventoryItem.objects.get(user=request.user, item=ingredient.ingredient)
                inv_item.adjust_quantity(-ingredient.quantity)

            # Add the crafted item to the inventory
            crafted_item = recipe.result_item
            inv_item, created = InventoryItem.objects.get_or_create(user=request.user, item=crafted_item)
            if not created:
                inv_item.adjust_quantity(recipe.result_quantity)
            else:
                inv_item.quantity = recipe.result_quantity
                inv_item.save()

        return JsonResponse(
            {"success": True, "message": f"Successfully crafted {recipe.result_quantity} x {crafted_item.name}!"})
    except Exception as e:
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)