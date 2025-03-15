from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from apps.crates.crate_definitions import CRATE_TYPES


class Crate(models.Model):
    """Represents a crate owned by a user, supporting stacking."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="crates")
    crate_type = models.CharField(
        max_length=50,
        choices=[(key, crate.name) for key, crate in CRATE_TYPES.items()],
        default="materials"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency_type = models.CharField(max_length=10, choices=[("main", "Main Currency"), ("farm", "Farm Currency")])
    quantity = models.PositiveIntegerField(default=1)
    is_opened = models.BooleanField(default=False)
    rewards = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def adjust_quantity(self, amount):
        """Increase or decrease crate quantity, deleting when zero."""
        self.quantity = max(0, self.quantity + amount)
        if self.quantity == 0:
            self.delete()
        else:
            self.save()

    def save(self, *args, **kwargs):
        """Automatically set price and currency type from crate definitions if not manually set."""
        if not self.price and self.crate_type in CRATE_TYPES:
            self.price = CRATE_TYPES[self.crate_type].price
            self.currency_type = CRATE_TYPES[self.crate_type].currency
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{CRATE_TYPES[self.crate_type].name} - {self.user.username} (x{self.quantity})"


from django.db import models
from decimal import Decimal
from apps.crates.crate_definitions import CRATE_TYPES

class Item(models.Model):
    """Represents an item that can be found in crates or earned elsewhere."""

    ITEM_TYPES = [
        ("material", "Material"),
        ("blueprint", "Blueprint"),
        ("special", "Special Item"),
        ("consumable", "Consumable"),
        ("currency", "Currency"),
        ("Seed", "Seed"),
        ("crop", "Crop"),
    ]

    RARITY_LEVELS = [
        (1, "Common"),
        (2, "Uncommon"),
        (3, "Rare"),
        (4, "Epic"),
        (5, "Legendary"),
        (6, "Mythic"),
    ]

    name = models.CharField(max_length=100, unique=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    rarity = models.IntegerField(choices=RARITY_LEVELS, default=1)
    rarity_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    is_stackable = models.BooleanField(default=True)
    base_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True, null=True)

    @classmethod
    def get_or_create_from_loot(cls, item_name):
        """Fetches or creates an item based on crate loot pool settings."""
        for crate in CRATE_TYPES.values():
            for loot in crate.loot_pool:  # Each loot is (item_name, item_type, base_rarity, drop_rate)
                if loot[0] == item_name:
                    base_rarity = loot[2]
                    item_type = loot[1]
                    # For currency items, optionally set a default base_value if desired.
                    defaults = {"item_type": item_type, "rarity": base_rarity}
                    if item_type == "currency":
                        defaults["base_value"] = Decimal("10.00")
                    return cls.objects.get_or_create(
                        name=item_name,
                        defaults=defaults
                    )[0]
        raise ValueError(f"Item {item_name} not found in loot pool!")

    @property
    def value(self):
        """Dynamically calculate item value based on rarity multiplier."""
        rarity_multipliers = {1: 1.0, 2: 1.5, 3: 2.5, 4: 5.0, 5: 10.0}
        multiplier = Decimal(rarity_multipliers.get(self.rarity, 1.0))
        return (self.base_value * multiplier).quantize(Decimal("0.01"))

    def __str__(self):
        return f"{self.name} ({self.get_item_type_display()}, {self.get_rarity_display()})"

def get_default_item():
    """Ensures a valid default item exists for migrations."""
    item, _ = Item.objects.get_or_create(name="Placeholder Item", defaults={"item_type": "material", "rarity": 1})
    return item.id

class InventoryItem(models.Model):
    """Tracks items owned by a user, supporting stacking."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inventory")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "item")

    def adjust_quantity(self, amount):
        """Increase or decrease crate quantity without deleting the record when quantity is zero."""
        self.quantity = max(0, self.quantity + amount)
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.item.name} x{self.quantity}"

class CrateOpeningHistory(models.Model):
    """Logs each crate opening event."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="crate_history")
    crate = models.ForeignKey(Crate, on_delete=models.SET_NULL, null=True, blank=True)
    crate_type = models.CharField(max_length=50)  # For redundancy
    reward_item = models.CharField(max_length=100)  # Store the name of the reward item
    reward_rarity = models.IntegerField()  # The adjusted rarity at open time
    opened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} opened {self.crate_type} and received {self.reward_item} ({self.reward_rarity})"