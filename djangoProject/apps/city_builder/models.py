from django.utils import timezone
from django.db import models, transaction
from django.contrib.auth.models import User
from decimal import Decimal

class City(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='city')
    name = models.CharField(max_length=100, default="My Eco City")
    sustainability_score = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    funds = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    # Define grid dimensions for the city (optional)
    grid_width = models.PositiveIntegerField(default=5)
    grid_height = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    def calculate_sustainability_score(self):
        """
        Sums the effective sustainability bonus of all buildings.
        You might choose to weight this further based on building size or other factors.
        """
        total = Decimal('0.00')
        for building in self.buildings.all():
            total += building.effective_sustainability_bonus
        self.sustainability_score = total
        self.save()
        return total

class BuildingTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    base_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    # Resource requirements can be stored as JSON, e.g. {"wood": 100, "stone": 50}
    resource_requirements = models.JSONField(default=dict, blank=True)
    sustainability_bonus = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    # Optionally, include an image for the blueprint
    image = models.ImageField(upload_to='building_templates/', blank=True, null=True)
    upgrade_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.00'))

    produces_resource = models.CharField(max_length=50, blank=True, null=True)  # e.g., "wood"
    production_rate = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))  # units per hour


    def __str__(self):
        return self.name
    
    def get_upgrade_cost(self, current_level):
        """
        Calculates the upgrade cost for a building. For example, if current_level is 1,
        the cost might be base_cost; if level 2, cost increases by the upgrade multiplier, etc.
        """
        cost = self.base_cost * (self.upgrade_multiplier ** Decimal(current_level))
        return cost.quantize(Decimal("0.01"))

class CityBuilding(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='buildings')
    template = models.ForeignKey(BuildingTemplate, on_delete=models.CASCADE, related_name='instances')
    x = models.PositiveIntegerField()  # X-coordinate in the grid
    y = models.PositiveIntegerField()  # Y-coordinate in the grid
    upgrade_level = models.PositiveIntegerField(default=1)
    built_at = models.DateTimeField(auto_now_add=True)
    last_collected = models.DateTimeField(default=timezone.now)  # new field


    class Meta:
        unique_together = ('city', 'x', 'y')
        ordering = ['x', 'y']

    def __str__(self):
        return f"{self.template.name} (Level {self.upgrade_level}) at ({self.x}, {self.y}) in {self.city}"
    
    @property
    def effective_sustainability_bonus(self):
        # Example: base bonus increased by the upgrade multiplier per level
        return self.template.sustainability_bonus * (self.template.upgrade_multiplier ** Decimal(self.upgrade_level - 1))
    
    def get_upgrade_material_requirements(self):
        """
        Compute the material requirements for the next upgrade.
        For example, for each material, the cost might be the base requirement times the current upgrade level.
        """
        base_req = self.template.resource_requirements  # Example: {"wood": 100, "metal": 50}
        # Multiply each requirement by the current upgrade level.
        return {material: qty * self.upgrade_level for material, qty in base_req.items()}
    
    def upgrade(self):
        cost = self.template.get_upgrade_cost(self.upgrade_level)
        required_materials = self.get_upgrade_material_requirements()
        missing = {}
        user = self.city.user
        for material, qty_required in required_materials.items():
            inv_item = user.inventory.filter(item__name__iexact=material).first()
            if not inv_item or inv_item.quantity < qty_required:
                current_qty = inv_item.quantity if inv_item else 0
                missing[material] = qty_required - current_qty
        if missing:
            print("Upgrade failed, missing materials:", missing)
            return False, cost, missing
        if self.city.funds < cost:
            missing['funds'] = cost - self.city.funds
            print("Upgrade failed, insufficient funds:", missing)
            return False, cost, missing
        from django.db import transaction
        with transaction.atomic():
            for material, qty_required in required_materials.items():
                inv_item = user.inventory.filter(item__name__iexact=material).first()
                inv_item.adjust_quantity(-qty_required)
            self.city.funds -= cost
            self.city.save()
            self.upgrade_level += 1
            self.save()
            self.city.calculate_sustainability_score()
        print("Upgrade successful, new level:", self.upgrade_level)
        return True, cost, {}
    
    def collect_production(self):
        """
        Calculates production since last collection, updates user's inventory, and resets last_collected.
        Returns the produced amount.
        """
        # Only buildings with production functionality.
        if not self.template.produces_resource or self.template.production_rate <= 0:
            return Decimal("0.00")
        now = timezone.now()
        time_elapsed = (now - self.last_collected).total_seconds() / 3600  # hours
        produced = self.template.production_rate * Decimal(time_elapsed)
        # Reset last_collected to now
        self.last_collected = now
        self.save()
        return produced