# apps/farm/views.py
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from decimal import Decimal
from apps.farm.models import Building, BuildingUpgradeHistory, BuildingTemplate
from apps.users.models import UserProfile
from apps.crates.models import InventoryItem


@login_required
def building_list(request):
    """
    List all buildings for the current user.
    If the user has no buildings, redirect them to choose starting buildings.
    """
    buildings = Building.objects.filter(user=request.user)
    if not buildings.exists():
        return redirect('choose_starting_buildings')
    return render(request, 'farm/building_list.html', {'buildings': buildings})


@login_required
def building_detail(request, building_id):
    """
    Display detailed information for a specific building.
    """
    building = get_object_or_404(Building, id=building_id, user=request.user)
    return render(request, 'farm/building_detail.html', {'building': building})


@login_required
def choose_starting_buildings(request):
    # If the user already has buildings, redirect them to the building list.
    if Building.objects.filter(user=request.user).exists():
        return redirect('building_list')

    if request.method == 'POST':
        # Get or create default templates
        greenhouse, _ = BuildingTemplate.objects.get_or_create(
            name="Basic Greenhouse",
            defaults={
                "description": "Your starter greenhouse for growing crops.",
                "base_upgrade_cost": 100.00
            }
        )
        barn, _ = BuildingTemplate.objects.get_or_create(
            name="Small Barn",
            defaults={
                "description": "A small barn to house your animals and store feed.",
                "base_upgrade_cost": 100.00
            }
        )

        # Create default buildings for the user.
        Building.objects.create(
            user=request.user,
            template=greenhouse,
            level=1
        )
        Building.objects.create(
            user=request.user,
            template=barn,
            level=1
        )
        messages.success(request, "Your farm has been started!")
        return redirect('building_list')

    return render(request, "farm/choose_starting_buildings.html")


@login_required
def upgrade_building(request, building_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    building = get_object_or_404(Building, id=building_id, user=request.user)
    next_level = building.level + 1
    upgrade_level = building.template.upgrade_levels.filter(level=next_level).first()
    if not upgrade_level:
        return JsonResponse({"error": "No upgrade available for the next level."}, status=400)

    user_profile = UserProfile.objects.get(user=request.user)
    currency_cost = upgrade_level.upgrade_currency_cost
    if user_profile.currency_balance < currency_cost:
        return JsonResponse({"error": "Insufficient currency for upgrade."}, status=400)

    # Check for blueprint requirement
    if upgrade_level.blueprint_required:
        try:
            blueprint_item = InventoryItem.objects.get(user=request.user, item=upgrade_level.blueprint_required)
            if blueprint_item.quantity < 1:
                return JsonResponse(
                    {"error": f"You need at least 1 {upgrade_level.blueprint_required.name} to upgrade."}, status=400)
        except InventoryItem.DoesNotExist:
            return JsonResponse(
                {"error": f"Blueprint {upgrade_level.blueprint_required.name} is required for upgrade."}, status=400)

    # Check material requirements...
    material_requirements = upgrade_level.material_requirements.all()
    missing_materials = []
    for req in material_requirements:
        try:
            inv_item = InventoryItem.objects.get(user=request.user, item=req.item)
        except InventoryItem.DoesNotExist:
            missing_materials.append(f"{req.item.name} (need {req.quantity_required})")
            continue
        if inv_item.quantity < req.quantity_required:
            missing_materials.append(f"{req.item.name} (need {req.quantity_required}, have {inv_item.quantity})")

    if missing_materials:
        return JsonResponse({
            "error": "Missing materials: " + ", ".join(missing_materials)
        }, status=400)

    # Proceed with upgrade in a transaction
    try:
        with transaction.atomic():
            # Deduct currency
            user_profile.deduct_currency(currency_cost,
                                         description=f"Upgrade cost for {building.template.name} to level {next_level}")

            # Deduct required materials
            for req in material_requirements:
                inv_item = InventoryItem.objects.get(user=request.user, item=req.item)
                inv_item.adjust_quantity(-req.quantity_required)

            # Optionally, deduct the blueprint if it's consumable, or just check its presence

            # Upgrade the building level
            old_level = building.level
            building.level = next_level
            building.save()

            BuildingUpgradeHistory.objects.create(
                building=building,
                previous_level=old_level,
                new_level=next_level
            )
    except Exception as e:
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({
        "success": True,
        "message": f"{building.template.name} upgraded from level {old_level} to {next_level}.",
        "new_level": next_level
    })


@login_required
def building_catalog(request):
    templates = BuildingTemplate.objects.all()

    # Get the set of building template IDs that the user has built.
    user_built_ids = set(request.user.buildings.values_list('template_id', flat=True))

    # Annotate each template with an 'unlocked' attribute.
    for template in templates:
        if template.prerequisite:
            # The building is unlocked if the user has built the prerequisite.
            template.unlocked = template.prerequisite.id in user_built_ids
        else:
            template.unlocked = True  # No prerequisite means always unlocked

    return render(request, "farm/building_catalog.html", {"templates": templates})

@login_required
def building_template_detail(request, template_id):
    template = get_object_or_404(BuildingTemplate, id=template_id)
    # If a prerequisite is required, check if the user has built it.
    if template.prerequisite:
        unlocked = request.user.buildings.filter(template=template.prerequisite).exists()
    else:
        unlocked = True
    return render(request, "farm/building_template_detail.html", {
        "template": template,
        "unlocked": unlocked
    })

@login_required
def purchase_building(request, template_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=400)

    template = get_object_or_404(BuildingTemplate, id=template_id)
    user_profile = UserProfile.objects.get(user=request.user)
    purchase_cost = template.base_upgrade_cost  # You can adjust this logic if needed

    # Check if user has sufficient funds
    if user_profile.currency_balance < purchase_cost:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": "Insufficient funds to purchase this building."}, status=400)
        else:
            messages.error(request, "Insufficient funds to purchase this building.")
            return redirect('building_template_detail', template_id=template.id)

    # Check for blueprint requirement in the template
    if template.blueprint_required:
        try:
            blueprint_inv = InventoryItem.objects.get(user=request.user, item=template.blueprint_required)
            if blueprint_inv.quantity < 1:
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({
                                            "error": f"You must have at least one {template.blueprint_required.name} to purchase this building."},
                                        status=400)
                else:
                    messages.error(request,
                                   f"You must have {template.blueprint_required.name} to purchase this building.")
                    return redirect('building_template_detail', template_id=template.id)
        except InventoryItem.DoesNotExist:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {"error": f"You must have {template.blueprint_required.name} to purchase this building."},
                    status=400)
            else:
                messages.error(request, f"You must have {template.blueprint_required.name} to purchase this building.")
                return redirect('building_template_detail', template_id=template.id)

    try:
        with transaction.atomic():
            user_profile.deduct_currency(purchase_cost, description=f"Purchase of {template.name}")
            building = Building.objects.create(user=request.user, template=template, level=1)
    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)
        else:
            messages.error(request, f"Unexpected error: {str(e)}")
            return redirect('building_template_detail', template_id=template.id)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "message": f"You have purchased {template.name}!",
            "building_id": building.id
        })
    else:
        messages.success(request, f"You have purchased {template.name}!")
        return redirect('building_list')
