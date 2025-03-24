# apps/crafting/management/commands/load_recipies.py

from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.crafting.models import Recipe, RecipeIngredient
from apps.crafting.recipie_definitions import RECIPE_DEFINITIONS
from apps.crates.models import Item

class Command(BaseCommand):
    help = "Loads recipe definitions into the database."

    def handle(self, *args, **options):
        self.stdout.write("Loading recipes...")
        for key, recipe_def in RECIPE_DEFINITIONS.items():
            # Create the result item if it doesn't exist
            result_item, created = Item.objects.get_or_create(
                name=recipe_def.result_item,
                defaults={
                    "item_type": "consumable",  # Adjust default type as needed
                    "rarity": 1,                # Default rarity
                    "base_value": Decimal("0.00"),
                    "description": recipe_def.description or "Created by recipe loader."
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Created result item '{recipe_def.result_item}' for recipe '{recipe_def.name}'."
                ))
            else:
                self.stdout.write(f"Using existing result item '{recipe_def.result_item}' for recipe '{recipe_def.name}'.")

            # Create or update the Recipe object
            recipe, created = Recipe.objects.get_or_create(
                name=recipe_def.name,
                defaults={
                    'result_item': result_item,
                    'result_quantity': recipe_def.result_quantity,
                    'description': recipe_def.description
                }
            )
            if not created:
                recipe.result_quantity = recipe_def.result_quantity
                recipe.description = recipe_def.description
                recipe.result_item = result_item
                recipe.save()
                self.stdout.write(f"Updated recipe: {recipe_def.name}")
            else:
                self.stdout.write(f"Created recipe: {recipe_def.name}")

            # Now, create or update RecipeIngredient objects.
            for ingredient_name, required_quantity in recipe_def.ingredients:
                ingredient_item, created = Item.objects.get_or_create(
                    name=ingredient_name,
                    defaults={
                        "item_type": "material",  # Default type (adjust as needed)
                        "rarity": 1,  # Default rarity
                        "base_value": Decimal("0.00"),  # Default value (or adjust if necessary)
                        "description": f"Created automatically for recipe '{recipe_def.name}'."
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Created missing ingredient '{ingredient_name}' for recipe '{recipe_def.name}'."
                    ))
                ri, ri_created = RecipeIngredient.objects.get_or_create(
                    recipe=recipe,
                    ingredient=ingredient_item,
                    defaults={'quantity': required_quantity}
                )
                if not ri_created:
                    ri.quantity = required_quantity
                    ri.save()
                    self.stdout.write(f"Updated ingredient '{ingredient_name}' for recipe '{recipe_def.name}'.")
                else:
                    self.stdout.write(f"Added ingredient '{ingredient_name}' for recipe '{recipe_def.name}'.")
        self.stdout.write(self.style.SUCCESS("Recipes loaded successfully!"))