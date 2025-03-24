# apps/farm/models.py

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from apps.crates.models import Item

class BuildingTemplate(models.Model):
    """
    Defines a type of building available in the game.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    base_upgrade_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("100.00"),
        help_text="Base currency cost for upgrading this building"
    )
    blueprint_required = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'item_type': 'blueprint'},
        help_text="Blueprint required for constructing this building"
    )
    prerequisite = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="unlocks",
        help_text="Building that must be built to unlock this building"
    )

    def __str__(self):
        return self.name


class BuildingUpgradeLevel(models.Model):
    """
    Represents the upgrade requirements for a building template at a specific level.
    Includes both a currency cost and (optionally) a blueprint requirement.
    """
    building_template = models.ForeignKey(
        BuildingTemplate,
        on_delete=models.CASCADE,
        related_name="upgrade_levels"
    )
    level = models.PositiveIntegerField(help_text="Upgrade level (starting at 1)")
    upgrade_currency_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Currency cost required for this upgrade"
    )
    # New optional field for blueprint requirement:
    blueprint_required = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'item_type': 'blueprint'},
        help_text="Optional blueprint required for this upgrade level"
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('building_template', 'level')
        ordering = ['level']

    def __str__(self):
        return f"{self.building_template.name} Level {self.level}"


class BuildingUpgradeMaterialRequirement(models.Model):
    """
    Represents the material requirements for a specific building upgrade level.
    """
    upgrade_level = models.ForeignKey(
        BuildingUpgradeLevel, on_delete=models.CASCADE, related_name="material_requirements"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity_required = models.PositiveIntegerField(default=1, help_text="Quantity of this item required")

    def __str__(self):
        return f"{self.quantity_required} x {self.item.name} for {self.upgrade_level}"


class Building(models.Model):
    """
    Represents a user's instance of a building, based on a BuildingTemplate.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buildings")
    template = models.ForeignKey(BuildingTemplate, on_delete=models.CASCADE, null=True)
    level = models.PositiveIntegerField(default=1)
    # Additional fields (production, efficiency, etc.) can be added here.

    def current_upgrade_cost(self):
        """
        Returns the currency cost for the next upgrade level.
        If no upgrade level is defined for the next level, returns None.
        """
        next_level = self.level + 1
        upgrade_level = self.template.upgrade_levels.filter(level=next_level).first()
        if upgrade_level:
            return upgrade_level.upgrade_currency_cost
        return None

    def next_level_material_requirements(self):
        """
        Returns the material requirements for the next upgrade level.
        """
        next_level = self.level + 1
        upgrade_level = self.template.upgrade_levels.filter(level=next_level).first()
        if upgrade_level:
            return upgrade_level.material_requirements.all()
        return None

    def __str__(self):
        return f"{self.template.name} (Level {self.level})"


# Optional: A model to track upgrade history.
class BuildingUpgradeHistory(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="upgrade_history")
    previous_level = models.PositiveIntegerField()
    new_level = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.building} upgraded from {self.previous_level} to {self.new_level} on {self.timestamp}"