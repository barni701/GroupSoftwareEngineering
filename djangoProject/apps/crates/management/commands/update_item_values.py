# apps/crates/management/commands/update_item_values.py
from django.core.management.base import BaseCommand
from apps.crates.models import Item
from decimal import Decimal

class Command(BaseCommand):
    help = "Updates base values for items based on item type"

    def handle(self, *args, **options):
        for item in Item.objects.all():
            if item.item_type == "material":
                item.base_value = Decimal("2.50")
            elif item.item_type == "blueprint":
                item.base_value = Decimal("10.00")
            elif item.item_type == "special":
                item.base_value = Decimal("15.00")
            else:
                item.base_value = Decimal("1.00")
            item.save()
            self.stdout.write(f"Updated {item.name} to base value {item.base_value}")
        self.stdout.write("Item values updated successfully!")