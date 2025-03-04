from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404, render

from apps.crates.models import Crate, InventoryItem, Item, CrateOpeningHistory
from apps.crates.crate_definitions import CRATE_TYPES
from apps.users.models import UserProfile


@login_required
def buy_crate(request, crate_type):
    """Handles crate purchasing, stacking crates instead of duplicating."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    user_profile = UserProfile.objects.get(user=request.user)
    crate_def = CRATE_TYPES.get(crate_type)

    if not crate_def:
        return JsonResponse({"error": "Invalid crate type"}, status=400)

    try:
        with transaction.atomic():
            # Deduct the correct currency
            if crate_def.currency == "main":
                if not user_profile.deduct_currency(crate_def.price, f"Purchased {crate_def.name} crate"):
                    return JsonResponse({"error": "Insufficient main currency"}, status=400)
            else:
                if not user_profile.deduct_farm_currency(crate_def.price, f"Purchased {crate_def.name} crate"):
                    return JsonResponse({"error": "Insufficient farm currency"}, status=400)

            # Check if the user already has this crate type
            crate, created = Crate.objects.get_or_create(
                user=request.user,
                crate_type=crate_type,
                defaults={"price": crate_def.price, "currency_type": crate_def.currency, "quantity": 0}
            )
            # Increase quantity using adjust_quantity instead of add_quantity
            crate.adjust_quantity(1)

        return JsonResponse({"success": True, "message": f"Purchased {crate_def.name} crate! (x{crate.quantity})"})

    except Exception as e:
        return JsonResponse({"error": f"Unexpected error: {e}"}, status=500)


@login_required
def open_crate(request, crate_type):
    """Handles crate opening, applies improved rarity system, and logs the event."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    crate = get_object_or_404(Crate, user=request.user, crate_type=crate_type)
    if crate.quantity < 1:
        return JsonResponse({"error": "No crates available to open."}, status=400)

    try:
        crate_def = CRATE_TYPES.get(crate_type)
        if not crate_def:
            return JsonResponse({"error": "Invalid crate type"}, status=400)

        # Get a rare item from the loot pool
        dropped_item_name = crate_def.get_random_drop()

        # Fetch the item using our utility method (based on loot pool settings)
        dropped_item = Item.get_or_create_from_loot(dropped_item_name)

        # Compute adjusted rarity dynamically (without altering the stored rarity)
        adjusted_rarity = min(5, int(dropped_item.rarity * crate_def.rarity_boost))

        # Add the item to inventory (stacking if it already exists)
        inventory_item, created = InventoryItem.objects.get_or_create(user=request.user, item=dropped_item)
        if not created:
            inventory_item.adjust_quantity(1)

        # Reduce crate quantity (adjust quantity without deleting the record)
        if crate.quantity > 1:
            crate.adjust_quantity(-1)
        else:
            crate.quantity = 0
            crate.save()

        # Log the crate opening event
        CrateOpeningHistory.objects.create(
            user=request.user,
            crate=crate,
            crate_type=crate_type,
            reward_item=dropped_item.name,
            reward_rarity=adjusted_rarity
        )

        return JsonResponse({
            "success": True,
            "reward": {
                "item": dropped_item.name,
                "rarity": adjusted_rarity
            }
        })
    except Exception as e:
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

@login_required
def crate_shop(request):
    """
    Renders the crate shop page.
    Passes the CRATE_TYPES dictionary to the template as 'crate_definitions'.
    """
    context = {
        "crate_definitions": CRATE_TYPES
    }
    return render(request, "crates/crate_shop.html", context)


@login_required
def bulk_open_crates(request, crate_type):
    """
    Opens all available crates of a given type for the user and returns a summary.
    This view repeatedly calls the open_crate logic.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    crate = Crate.objects.filter(user=request.user, crate_type=crate_type).first()
    if not crate or crate.quantity < 1:
        return JsonResponse({"error": "No crates available to open."}, status=400)

    rewards = []
    # Loop until the crate is out of stock
    while crate.quantity > 0:
        # We simulate opening a crate by calling the open_crate view logic directly
        # Alternatively, you could call a helper function for this.
        response = open_crate(request, crate_type)
        data = response.json()
        if data.get("success"):
            rewards.append(data["reward"])
        else:
            break  # Stop if any error occurs
        # Refresh the crate instance
        crate = Crate.objects.filter(user=request.user, crate_type=crate_type).first()
        if not crate:
            break

    return JsonResponse({"success": True, "rewards": rewards})

@login_required
def crate_inventory(request):
    """Displays all crates owned by the user."""
    user_crates = Crate.objects.filter(user=request.user, quantity__gt=0)
    return render(request, "crates/inventory.html", {"crates": user_crates})

@login_required
def item_inventory(request):
    """Displays all items in the user's inventory."""
    inventory_items = InventoryItem.objects.filter(user=request.user)
    return render(request, "crates/item_inventory.html", {"inventory_items": inventory_items})