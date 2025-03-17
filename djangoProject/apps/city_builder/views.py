from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from .models import City, BuildingTemplate, CityBuilding
from apps.users.models import UserProfile

@login_required
def city_dashboard(request):
    try:
        city = request.user.city
    except City.DoesNotExist:
        city = City.objects.create(user=request.user, funds=Decimal("500.00"))
    
    # Optionally recalc sustainability score.
    city.calculate_sustainability_score()
    
    # Get all buildings for this city.
    buildings = city.buildings.all()

    # Build a grid based on city.grid_width and city.grid_height.
    grid = []
    for y in range(city.grid_height):
        row = []
        for x in range(city.grid_width):
            # Filter for a building at the given coordinate.
            building = buildings.filter(x=x, y=y).first()
            row.append(building)
        grid.append(row)

    materials = request.user.inventory.filter(item__item_type="material")
    blueprints = request.user.inventory.filter(item__item_type="blueprint")
    
    context = {
        "city": city,
        "grid": grid,
        "materials": materials,
        "blueprints": blueprints,
    }
    return render(request, "city_builder/dashboard.html", context)

@login_required
def building_catalog(request):
    """
    Displays a list of all available building templates.
    """
    templates = BuildingTemplate.objects.all()
    context = {
        "templates": templates,
    }
    return render(request, "city_builder/catalog.html", context)

@login_required
def building_template_detail(request, template_id):
    template_obj = get_object_or_404(BuildingTemplate, id=template_id)
    # Filter only for material type items
    materials = request.user.inventory.filter(item__item_type="material")
    context = {
        "template": template_obj,
        "materials": materials,
    }
    return render(request, "city_builder/building_detail.html", context)

@login_required
def construct_building(request, template_id):
    """
    Constructs a building in the user's city at specified grid coordinates.
    Deducts the cost from the city's funds.
    """
    template_obj = get_object_or_404(BuildingTemplate, id=template_id)
    city = request.user.city  # Assumes a city already exists.
    
    # Build a list of occupied coordinates from the user's existing buildings.
    occupied = [f"{b.x},{b.y}" for b in city.buildings.all()]
    
    if request.method == "POST":
        try:
            x = int(request.POST.get("x"))
            y = int(request.POST.get("y"))
        except (TypeError, ValueError):
            messages.error(request, "Invalid grid coordinates.")
            return redirect("building_template_detail", template_id=template_id)
        
        # Check that coordinates fall within city grid boundaries.
        if x < 0 or x >= city.grid_width or y < 0 or y >= city.grid_height:
            messages.error(request, "Coordinates are out of the valid grid bounds.")
            return redirect("building_template_detail", template_id=template_id)
        
        # Check if that grid cell is available.
        if CityBuilding.objects.filter(city=city, x=x, y=y).exists():
            messages.error(request, "This plot is already occupied.")
            return redirect("building_template_detail", template_id=template_id)
        
        cost = template_obj.base_cost
        if city.funds < cost:
            messages.error(request, "Insufficient funds to construct this building.")
            return redirect("building_template_detail", template_id=template_id)
        
        # Use an atomic transaction for funds deduction and building creation.
        try:
            with transaction.atomic():
                city.funds -= cost
                city.save()
                building = CityBuilding.objects.create(
                    city=city,
                    template=template_obj,
                    x=x,
                    y=y,
                    upgrade_level=1,
                )
                city.calculate_sustainability_score()
        except Exception as e:
            messages.error(request, f"Error constructing building: {str(e)}")
            return redirect("building_template_detail", template_id=template_id)
        
        messages.success(request, f"{template_obj.name} constructed at ({x}, {y})!")
        return redirect("city_dashboard")
    
    # Pass both the template and the occupied coordinates to the context.
    context = {
        "template": template_obj,
        "occupied": occupied,
    }
    return render(request, "city_builder/construct_building.html", context)

@login_required
def upgrade_building(request, building_id):
    building = get_object_or_404(CityBuilding, id=building_id, city=request.user.city)
    if request.method == "POST":
        success, cost, missing = building.upgrade()
        if success:
            messages.success(request, f"{building.template.name} upgraded to level {building.upgrade_level} at a cost of ${cost}.")
        else:
            if 'funds' in missing:
                messages.error(request, f"Insufficient funds for upgrade. Additional funds needed: ${missing['funds']}.")
            elif missing:
                missing_str = ", ".join(f"{mat}: {qty}" for mat, qty in missing.items())
                messages.error(request, f"Insufficient materials for upgrade. Missing: {missing_str}.")
            else:
                messages.error(request, "Upgrade failed due to unknown reasons.")
        return redirect("city_dashboard")
    
    # Calculate the upgrade cost for the current level.
    upgrade_cost = building.template.get_upgrade_cost(building.upgrade_level)
    # Get required materials for upgrade (assumed to be a dictionary)
    upgrade_materials = building.get_upgrade_material_requirements()
    # Build a dictionary for inventory materials for material items.
    inventory_materials = {}
    for inv_item in request.user.inventory.filter(item__item_type="material"):
        inventory_materials[inv_item.item.name.lower()] = inv_item.quantity

    context = {
        "building": building,
        "upgrade_cost": upgrade_cost,
        "upgrade_materials": upgrade_materials,
        "inventory_materials": inventory_materials,
    }
    return render(request, "city_builder/upgrade_building.html", context)

@login_required
def add_city_funds(request):
    if request.method == "POST":
        try:
            amount = Decimal(request.POST.get("amount", "0"))
        except Exception:
            messages.error(request, "Invalid amount entered.")
            return redirect("city_dashboard")
        if amount <= 0:
            messages.error(request, "Please enter a positive amount.")
            return redirect("city_dashboard")
        user_profile = request.user.userprofile
        if user_profile.currency_balance < amount:
            messages.error(request, "Insufficient funds in your account.")
            return redirect("city_dashboard")
        # Deduct from user's personal currency and add to city funds.
        if not user_profile.deduct_currency(amount, "Invest in City Funds"):
            messages.error(request, "Error processing your transaction.")
            return redirect("city_dashboard")
        city = request.user.city  # Assuming each user has a City instance.
        city.funds += amount
        city.save()
        messages.success(request, f"Successfully added ${amount} to your city funds.")
        return redirect("city_dashboard")
    
    return render(request, "city_builder/add_funds.html")

@login_required
def collect_production(request, building_id):
    building = get_object_or_404(CityBuilding, id=building_id, city=request.user.city)
    produced = building.collect_production()
    if produced > 0:
        # For example, add the produced resource to user's inventory.
        resource_name = building.template.produces_resource
        user = request.user
        # Get or create the inventory item.
        inv_item, _ = user.inventory.get_or_create(
            item__name__iexact=resource_name,
            defaults={"item": {"name": resource_name, "item_type": "material"}, "quantity": 0}
        )
        # Alternatively, if you have a proper Item model, do:
        from apps.crates.models import Item, InventoryItem
        item_obj, _ = Item.objects.get_or_create(name=resource_name, defaults={"item_type": "material", "rarity": 1, "base_value": Decimal("1.00")})
        inv_item, created = InventoryItem.objects.get_or_create(user=user, item=item_obj, defaults={"quantity": 0})
        inv_item.adjust_quantity(produced)
        messages.success(request, f"Collected {produced:.2f} units of {resource_name}.")
    else:
        messages.info(request, "No production available at this time.")
    return redirect("city_dashboard")

@login_required
def material_dashboard(request):
    # Filter inventory items for materials only (assuming "material" is the item_type for these)
    materials = request.user.inventory.filter(item__item_type="material")
    context = {
        "materials": materials,
    }
    return render(request, "city_builder/material_dashboard.html", context)