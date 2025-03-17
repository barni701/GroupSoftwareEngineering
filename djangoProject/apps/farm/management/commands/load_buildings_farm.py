from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.farm.models import (
    BuildingTemplate,
    BuildingUpgradeLevel,
    BuildingUpgradeMaterialRequirement
)
from apps.crates.models import Item

# Define your building templates and upgrade levels
BUILDING_DEFINITIONS = [
    {
        "name": "Greenhouse",
        "description": "A facility for growing crops in a controlled environment.",
        "base_upgrade_cost": "100.00",
        "blueprint_required": "Greenhouse Blueprint",  # Optional blueprint for the template
        "upgrade_levels": [
            {
                "level": 2,
                "upgrade_cost": "150.00",
                "blueprint_required": "Greenhouse Blueprint Level 2",  # Optional blueprint for upgrade level 2
                "material_requirements": [
                    {"item": "Glass", "quantity": 20},
                    {"item": "Wood", "quantity": 10}
                ]
            },
            {
                "level": 3,
                "upgrade_cost": "225.00",
                "material_requirements": [
                    {"item": "Glass", "quantity": 30},
                    {"item": "Wood", "quantity": 15}
                ]
            },
            {
                "level": 4,
                "upgrade_cost": "337.50",
                "blueprint_required": "Greenhouse Blueprint Level 4",
                "material_requirements": [
                    {"item": "Glass", "quantity": 40},
                    {"item": "Wood", "quantity": 20},
                    {"item": "Metal", "quantity": 5}
                ]
            },
        ]
    },
    {
        "name": "Barn",
        "description": "Storage and animal housing.",
        "base_upgrade_cost": "80.00",
        "blueprint_required": "Barn Blueprint",  # Optional for Barn template
        "upgrade_levels": [
            {
                "level": 2,
                "upgrade_cost": "120.00",
                "material_requirements": [
                    {"item": "Wood", "quantity": 30},
                    {"item": "Stone", "quantity": 10}
                ]
            },
            {
                "level": 3,
                "upgrade_cost": "180.00",
                "blueprint_required": "Barn Blueprint Level 3",
                "material_requirements": [
                    {"item": "Wood", "quantity": 40},
                    {"item": "Stone", "quantity": 15}
                ]
            },
        ]
    },
    # Add additional building definitions as needed.
]

class Command(BaseCommand):
    help = "Loads building templates, upgrade levels, material requirements, and blueprint requirements."

    def handle(self, *args, **options):
        for definition in BUILDING_DEFINITIONS:
            # Process optional blueprint for the template.
            blueprint_item = None
            if "blueprint_required" in definition:
                blueprint_name = definition["blueprint_required"]
                blueprint_item, _ = Item.objects.get_or_create(
                    name=blueprint_name,
                    defaults={
                        "item_type": "blueprint",
                        "rarity": 1,  # Adjust as needed
                        "base_value": Decimal("0.00"),
                        "description": f"Automatically created for {definition['name']} template."
                    }
                )

            template_defaults = {
                "description": definition["description"],
                "base_upgrade_cost": Decimal(definition["base_upgrade_cost"])
            }
            if blueprint_item:
                template_defaults["blueprint_required"] = blueprint_item

            template, created = BuildingTemplate.objects.get_or_create(
                name=definition["name"],
                defaults=template_defaults
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created BuildingTemplate: {template.name}"))
            else:
                self.stdout.write(f"BuildingTemplate {template.name} already exists.")

            # Process upgrade levels for this template.
            for upgrade_def in definition.get("upgrade_levels", []):
                upgrade_defaults = {
                    "upgrade_currency_cost": Decimal(upgrade_def["upgrade_cost"]),
                    "description": f"Upgrade to level {upgrade_def['level']}"
                }
                # Check if this upgrade level requires a blueprint.
                if "blueprint_required" in upgrade_def:
                    bp_name = upgrade_def["blueprint_required"]
                    bp_item, _ = Item.objects.get_or_create(
                        name=bp_name,
                        defaults={
                            "item_type": "blueprint",
                            "rarity": 1,  # Adjust as needed
                            "base_value": Decimal("0.00"),
                            "description": f"Automatically created for {template.name} upgrade level {upgrade_def['level']}"
                        }
                    )
                    upgrade_defaults["blueprint_required"] = bp_item

                upgrade_level, created = BuildingUpgradeLevel.objects.get_or_create(
                    building_template=template,
                    level=upgrade_def["level"],
                    defaults=upgrade_defaults
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Created Upgrade Level {upgrade_level.level} for {template.name}"
                    ))
                else:
                    self.stdout.write(
                        f"Upgrade Level {upgrade_level.level} for {template.name} already exists."
                    )

                # Process material requirements for the upgrade level.
                for req in upgrade_def.get("material_requirements", []):
                    item, _ = Item.objects.get_or_create(
                        name=req["item"],
                        defaults={
                            "item_type": "material",
                            "rarity": 1,
                            "base_value": Decimal("0.00"),
                            "description": f"Automatically created for {template.name} upgrade requirements."
                        }
                    )
                    requirement, created = BuildingUpgradeMaterialRequirement.objects.get_or_create(
                        upgrade_level=upgrade_level,
                        item=item,
                        defaults={"quantity_required": req["quantity"]}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f"Created Material Requirement: {req['quantity']} x {req['item']} for {template.name} level {upgrade_def['level']}"
                        ))
                    else:
                        self.stdout.write(
                            f"Material Requirement for {req['item']} at {template.name} level {upgrade_def['level']} already exists."
                        )

        self.stdout.write(self.style.SUCCESS("Building templates and upgrade levels loaded successfully!"))