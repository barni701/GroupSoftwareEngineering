from django.db import models
from django.utils import timezone
from decimal import Decimal
from ..users.models import UserProfile

class Farm(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    production_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))  # New currency per hour
    last_collected = models.DateTimeField(auto_now=True)

    def collect_farm_currency(self):
        """Calculate generated farm currency and update user balance."""
        now = timezone.now()
        hours_passed = (now - self.last_collected).total_seconds() / 3600
        earned_currency = self.production_rate * Decimal(hours_passed)

        if earned_currency > 0:
            self.user.add_farm_currency(earned_currency, description="Farm production")
            self.last_collected = now
            self.save()

        return earned_currency

class Blueprint(models.Model):
    name = models.CharField(max_length=100)
    rarity = models.CharField(max_length=20, choices=[("common", "Common"), ("rare", "Rare"), ("legendary", "Legendary")])
    upgrade_effect = models.TextField()  # Could store JSON for dynamic effects
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # Cost in farm currency

    def apply_upgrade(self, farm):
        """Apply the blueprint upgrade to a farm."""
        if farm.user.currency_balance >= self.cost:
            farm.user.deduct_currency(self.cost, description=f"Purchased {self.name} blueprint")
            farm.production_rate += Decimal('1.5')  # Example: Increase production rate
            farm.save()
            return True
        return False