from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from decimal import Decimal
from apps.crates.models import Crate
from django.shortcuts import render
import random

from apps.users.models import UserProfile


@login_required
@csrf_exempt
def open_crate(request, crate_id):
    """Handles crate opening and distributes rewards."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    crate = get_object_or_404(Crate, id=crate_id, user=request.user, is_opened=False)

    # Ensure the crate has a defined type before opening
    if not crate.type:
        return JsonResponse({"error": "Crate type is missing"}, status=400)

    reward = crate.open()  # Call the crate's open() method

    # Check if reward is properly generated
    if not reward:
        return JsonResponse({"success": False, "error": "No reward found"}, status=500)

    return JsonResponse({
        "success": True,
        "reward": reward
    })

@login_required
def crate_inventory(request):
    """Display the user's available crates."""
    user_crates = Crate.objects.filter(user=request.user, is_opened=False)
    return render(request, "crates/crate_inventory.html", {"crates": user_crates})

@login_required
def crate_history(request):
    """Displays a history of opened crates and rewards"""
    opened_crates = Crate.objects.filter(user=request.user, is_opened=True).order_by("-id")
    return render(request, "crates/crate_open_history.html", {"history": opened_crates})


@login_required
def crate_shop(request):
    """Displays available crates for purchase."""
    available_crates = [
        {"type": "materials", "price": Decimal("10.00"), "currency": "main"},
        {"type": "blueprint", "price": Decimal("15.00"), "currency": "farm"},
    ]
    return render(request, "crates/crate_shop.html", {"crates": available_crates})


@login_required
def buy_crate(request, crate_type):
    """Handles crate purchasing logic."""
    user_profile = UserProfile.objects.get(user=request.user)

    # Define crate prices (could be dynamic in a real-world case)
    crate_prices = {
        "materials": {"price": Decimal("10.00"), "currency": "main"},
        "blueprint": {"price": Decimal("15.00"), "currency": "farm"},
    }

    if crate_type not in crate_prices:
        return JsonResponse({"error": "Invalid crate type"}, status=400)

    crate_price = crate_prices[crate_type]["price"]
    currency_type = crate_prices[crate_type]["currency"]

    # Deduct the correct currency and add crate to user account
    if currency_type == "main":
        if not user_profile.deduct_currency(crate_price, f"Purchased {crate_type} crate"):
            return JsonResponse({"error": "Insufficient funds"}, status=400)
    else:
        if not user_profile.deduct_farm_currency(crate_price, f"Purchased {crate_type} crate"):
            return JsonResponse({"error": "Insufficient farm currency"}, status=400)

    # Assign a new crate to the user
    new_crate = Crate.objects.create(user=request.user, type=crate_type, is_opened=False, price=crate_price,
                                     currency_type=currency_type)

    return JsonResponse({"success": True, "message": f"Purchased {crate_type} crate!"})