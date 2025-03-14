# apps/garden/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.garden.models import GardenPlot, GardenPlant
from apps.crates.models import InventoryItem
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

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
    base_duration = timedelta(hours=2)
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

@login_required
def create_plot(request):
    if request.method == "POST":
        # Get a plot name from the POST data, or use a default name.
        name = request.POST.get("name", "New Plot")
        # Create a new plot for the user.
        GardenPlot.objects.create(user=request.user, name=name)
        messages.success(request, "New garden plot created!")
        return redirect("garden_dashboard")
    return render(request, "garden/create_plot.html")

@login_required
def harvest_crop(request, plant_id):
    # Retrieve the plant instance for the user
    plant = get_object_or_404(GardenPlant, id=plant_id, user=request.user)
    
    # Check if the plant is ready to harvest
    if not plant.is_ready_to_harvest():
        messages.error(request, "This crop is not ready for harvest yet.")
        return redirect('garden_dashboard')
    
    # Mark the plant as harvested
    plant.is_harvested = True
    plant.save()
    
    # Free up the plot by setting current_plant to None if it exists
    if hasattr(plant, 'plot') and plant.plot is not None:
        plot = plant.plot
        plot.current_plant = None
        plot.save()
    
    messages.success(request, f"You have successfully harvested {plant.seed.name}!")
    return redirect('garden_dashboard')