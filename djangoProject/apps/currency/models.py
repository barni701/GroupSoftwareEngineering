from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class CurrencyAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

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