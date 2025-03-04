import random

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
    """Handles crate opening, applies improved rarity system, logs the event, and processes currency rewards."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    crate = get_object_or_404(Crate, user=request.user, crate_type=crate_type)
    if crate.quantity < 1:
        return JsonResponse({"error": "No crates available to open."}, status=400)

    try:
        crate_def = CRATE_TYPES.get(crate_type)
        if not crate_def:
            return JsonResponse({"error": "Invalid crate type"}, status=400)

        # Get the full loot tuple (includes optional value range)
        loot = crate_def.get_random_loot()  # e.g., ("Eco Tokens", "currency", 2, 50, (2,4))
        print("DEBUG: Loot tuple:", loot)
        dropped_item_name = loot[0]

        # Fetch the item using our utility method
        dropped_item = Item.get_or_create_from_loot(dropped_item_name)
        print("DEBUG: Dropped item:", dropped_item.name, dropped_item.item_type, dropped_item.rarity)

        # Compute adjusted rarity dynamically without altering stored rarity
        adjusted_rarity = min(5, int(dropped_item.rarity * crate_def.rarity_boost))
        rarity_display = dict(Item.RARITY_LEVELS).get(adjusted_rarity, str(adjusted_rarity))

        # Get user profile
        user_profile = UserProfile.objects.get(user=request.user)

        # Process currency rewards if the item type is currency and a value range is provided.
        if dropped_item.item_type == "currency" and len(loot) >= 5:
            value_range = loot[4]  # Expected as a tuple (min, max)
            reward_amount = round(random.uniform(*value_range), 2)
            print("DEBUG: Currency drop detected. Value range:", value_range, "Reward amount:", reward_amount)
            user_profile.add_farm_currency(reward_amount, description="Crate Opening Reward")
            reward_info = {
                "item": dropped_item.name,
                "rarity": rarity_display,
                "farm_currency_awarded": reward_amount
            }
        else:
            # Otherwise, add the item to inventory
            inventory_item, created = InventoryItem.objects.get_or_create(user=request.user, item=dropped_item)
            if not created:
                inventory_item.adjust_quantity(1)
            reward_info = {
                "item": dropped_item.name,
                "rarity": rarity_display
            }

        # Reduce crate quantity without deleting the record
        if crate.quantity > 1:
            crate.adjust_quantity(-1)
        else:
            crate.quantity = 0
            crate.save()

        # Log the opening event if desired
        CrateOpeningHistory.objects.create(
            user=request.user,
            crate=crate,
            crate_type=crate_type,
            reward_item=dropped_item.name,
            reward_rarity=adjusted_rarity
        )

        return JsonResponse({
            "success": True,
            "reward": reward_info,
            "remaining": crate.quantity
        })
    except Exception as e:
        print("DEBUG: Exception in open_crate:", str(e))
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


def process_single_crate_opening(user, crate, crate_def):
    """
    Processes a single crate opening.
    Returns a dictionary with reward info.
    Assumes that:
      - If the dropped item is of type "currency" and a value range is provided in the loot tuple,
        a random reward amount is generated and added to the user's farm currency.
      - Otherwise, the item is added to the user's inventory.
    """
    # Get the full loot tuple (with optional value range)
    loot = crate_def.get_random_loot()  # e.g. ("Eco-Tokens", "currency", 2, 50, (1, 4))
    dropped_item_name = loot[0]

    # Fetch the item based on loot settings
    dropped_item = Item.get_or_create_from_loot(dropped_item_name)

    # Compute adjusted rarity
    adjusted_rarity = min(5, int(dropped_item.rarity * crate_def.rarity_boost))
    rarity_display = dict(Item.RARITY_LEVELS).get(adjusted_rarity, str(adjusted_rarity))

    # Get the user's profile
    user_profile = UserProfile.objects.get(user=user)

    # Process currency rewards if applicable
    if dropped_item.item_type == "currency" and len(loot) >= 5:
        value_range = loot[4]  # tuple (min, max)
        reward_amount = round(random.uniform(*value_range), 2)
        user_profile.add_farm_currency(reward_amount, description="Bulk crate opening reward")
        reward_info = {
            "item": dropped_item.name,
            "rarity": rarity_display,
            "farm_currency_awarded": reward_amount
        }
    else:
        # Otherwise, add item to inventory (stacking if exists)
        inventory_item, created = InventoryItem.objects.get_or_create(user=user, item=dropped_item)
        if not created:
            inventory_item.adjust_quantity(1)
        reward_info = {
            "item": dropped_item.name,
            "rarity": rarity_display
        }

    # Reduce the crate's quantity
    crate.adjust_quantity(-1)

    return reward_info


@login_required
def bulk_open_crates(request, crate_type):
    """
    Opens all available crates of a given type for the user.
    Aggregates rewards so that repeated drops stack together.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    crate = Crate.objects.filter(user=request.user, crate_type=crate_type).first()
    if not crate or crate.quantity < 1:
        return JsonResponse({"error": "No crates available to open."}, status=400)

    crate_def = CRATE_TYPES.get(crate_type)
    if not crate_def:
        return JsonResponse({"error": "Invalid crate type"}, status=400)

    aggregated_rewards = {}  # key: item name; value: dict with aggregated info

    while crate and crate.quantity > 0:
        try:
            reward_info = process_single_crate_opening(request.user, crate, crate_def)
            key = reward_info.get("item")
            if key in aggregated_rewards:
                aggregated_rewards[key]["count"] += 1
                if "farm_currency_awarded" in reward_info:
                    aggregated_rewards[key]["farm_currency_awarded"] += reward_info["farm_currency_awarded"]
            else:
                aggregated_rewards[key] = reward_info.copy()
                aggregated_rewards[key]["count"] = 1
        except Exception as e:
            aggregated_rewards.setdefault("errors", []).append(str(e))
            break
        # Refresh the crate instance for the next iteration
        crate = Crate.objects.filter(user=request.user, crate_type=crate_type).first()

    # Convert aggregated_rewards dict to a list
    aggregated_list = list(aggregated_rewards.values())
    remaining = crate.quantity if crate else 0
    return JsonResponse({"success": True, "rewards": aggregated_list, "remaining": remaining})

    rewards = []
    # Process crate openings until none remain
    while crate and crate.quantity > 0:
        try:
            reward_info = process_single_crate_opening(request.user, crate, crate_def)
            rewards.append(reward_info)
            # Refresh the crate instance for the next iteration
            crate = Crate.objects.filter(user=request.user, crate_type=crate_type).first()
        except Exception as e:
            rewards.append({"error": f"Error processing crate: {str(e)}"})
            break  # Exit loop on error

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