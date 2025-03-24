# apps/garden/views.py

from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.garden.models import GardenPlot, GardenPlant
from apps.crates.models import InventoryItem
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from apps.users.utils import add_xp
from apps.users.models import UserProfile

@login_required
def garden_dashboard(request):
    plots = GardenPlot.objects.filter(user=request.user)
    # Find an empty plot (if any)
    empty_plot = GardenPlot.objects.filter(user=request.user, current_plant__isnull=True).first()
    return render(request, "garden/garden_dashboard.html", {
        "plots": plots,
        "empty_plot": empty_plot
    })

@login_required
def available_seeds(request, plot_id):
    # Retrieve the selected plot for the current user
    plot = get_object_or_404(GardenPlot, id=plot_id, user=request.user)
    # Optionally, you can check if the plot is empty:
    if plot.current_plant:
        messages.error(request, "This plot is already occupied. Please choose a different plot.")
        return redirect("garden_dashboard")
    # Retrieve available seed inventory for the user
    seeds = InventoryItem.objects.filter(user=request.user, item__item_type="seed", quantity__gt=0)
    return render(request, "garden/available_seeds.html", {"seeds": seeds, "selected_plot": plot})

@login_required
def plant_seed(request, plot_id, seed_id):
    plot = get_object_or_404(GardenPlot, id=plot_id, user=request.user)
    inv_item = get_object_or_404(InventoryItem, user=request.user, item__id=seed_id, item__item_type="seed")
    
    if inv_item.quantity < 1:
        messages.error(request, "You do not have any of that seed.")
        return redirect("available_seeds", plot_id=plot_id)
    
    if plot.current_plant:
        messages.error(request, "This plot is already occupied.")
        return redirect("garden_dashboard")
    
    # Define a base growth time of 2 hours.
    base_duration = timedelta(seconds=2)
    # Calculate multiplier: for rarity 1, multiplier = 1; for rarity 2, multiplier = 1.5; etc.
    multiplier = 1 + ((inv_item.item.rarity - 1) * 0.5)
    growth_duration = base_duration * multiplier
    
    plant = GardenPlant.objects.create(
        user=request.user,
        seed=inv_item.item,
        planted_at=timezone.now(),
        growth_duration=growth_duration
    )
    
    inv_item.adjust_quantity(-1)
    plot.current_plant = plant
    plot.save()
    
    messages.success(request, f"You planted {inv_item.item.name} in {plot.name}! It will be ready in {growth_duration}.")
    return redirect("garden_dashboard")

FREE_PLOT_LIMIT = 3
BASE_ADDITIONAL_PLOT_COST = Decimal("100")
GROWTH_FACTOR = Decimal("2")

@login_required
def create_plot(request):
    # Count how many plots the user already has
    current_plot_count = GardenPlot.objects.filter(user=request.user).count()
    
    # Compute cost if user has reached free limit
    if current_plot_count >= FREE_PLOT_LIMIT:
        extra_plots = current_plot_count - FREE_PLOT_LIMIT
        plot_cost = BASE_ADDITIONAL_PLOT_COST * (GROWTH_FACTOR ** extra_plots)
    else:
        plot_cost = Decimal("0.00")
    
    if request.method == "POST":
        # If there's a cost (i.e. user has reached free limit), ensure they have enough funds
        user_profile = request.user.userprofile
        if plot_cost > 0 and user_profile.currency_balance < plot_cost:
            messages.error(request, f"You don't have enough funds to create an additional plot (Cost: ${plot_cost}).")
            return redirect("garden_dashboard")
        if plot_cost > 0:
            # Deduct the cost from the user's currency balance.
            if not user_profile.deduct_currency(plot_cost, description="Purchase additional garden plot"):
                messages.error(request, "There was an error processing your payment.")
                return redirect("garden_dashboard")
        # Create the new plot with the provided name (or a default)
        name = request.POST.get("name", "New Plot")
        GardenPlot.objects.create(user=request.user, name=name)
        messages.success(request, "New garden plot created!")
        return redirect("garden_dashboard")
    
    # For GET requests, pass the computed cost to the template.
    context = {
        "plot_cost": plot_cost,
        "free_limit": FREE_PLOT_LIMIT,
        "current_plot_count": current_plot_count,
    }
    return render(request, "garden/create_plot.html", context)

'''@login_required
def create_plot(request):
    if request.method == "POST":
        # Get a plot name from the POST data, or use a default name.
        name = request.POST.get("name", "New Plot")
        # Create a new plot for the user.
        GardenPlot.objects.create(user=request.user, name=name)
        messages.success(request, "New garden plot created!")
        return redirect("garden_dashboard")
    return render(request, "garden/create_plot.html")'''

@login_required
def harvest_crop(request, plant_id):
    # Retrieve the plant instance for the user
    plant = get_object_or_404(GardenPlant, id=plant_id, user=request.user)
    
    # Check if the plant is ready to harvest
    if not plant.is_ready_to_harvest():
        messages.error(request, "This crop is not ready for harvest yet.")
        return redirect('garden_dashboard')
    
    # Mark the plant as harvested and save
    plant.is_harvested = True
    plant.save()
    
    # Free up the plot by clearing the current_plant field
    if hasattr(plant, 'plot') and plant.plot is not None:
        plot = plant.plot
        plot.current_plant = None
        plot.save()
    
    # Determine the harvested product name.
    # Here we assume that the crop name is the seed's name plus " Crop".
    harvested_product_name = f"{plant.seed.name} Crop"
    
    # Import Item and InventoryItem from your crates app.
    from apps.crates.models import Item, InventoryItem

    # Get or create the crop item.
    crop_item, created = Item.objects.get_or_create(
        name=harvested_product_name,
        defaults={
            "item_type": "crop", 
            "rarity": plant.seed.rarity,
            "base_value": plant.seed.base_value,
            "description": f"Harvested crop from {plant.seed.name}"
        }
    )
    
    # Get or create the inventory item and update quantity.
    inv_item, created = InventoryItem.objects.get_or_create(
        user=request.user,
        item=crop_item
    )
    inv_item.adjust_quantity(1)

    # Award XP using the centralized add_xp function
    xp_gain = plant.seed.rarity * 10  # For example: 10 XP per rarity point
    add_xp(request.user, xp_gain)
    
    messages.success(request, f"You have successfully harvested {plant.seed.name}! {harvested_product_name} has been added to your inventory.")
    return redirect('garden_dashboard')