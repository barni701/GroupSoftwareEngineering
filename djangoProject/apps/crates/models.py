import random
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from apps.users.models import UserProfile  # Import user profile

class Crate(models.Model):
    TYPE_CHOICES = [
        ("materials", "Materials Crate"),
        ("blueprint", "Blueprint Crate")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # Only assigned after purchase
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_opened = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("10.00"))  # Default crate price
    currency_type = models.CharField(
        max_length=10,
        choices=[("main", "Main Currency"), ("farm", "Farm Currency")],
        default="main"
    )  # Determines which currency is used

    def __str__(self):
        return f"{self.get_type_display()} - {self.price} ({self.currency_type})"

    def open(self):
        """Handles crate opening logic and rewards"""
        if self.is_opened:
            return None  # Prevent re-opening

        self.is_opened = True
        self.save()

        if self.type == "materials":
            return self.give_materials()
        elif self.type == "blueprint":
            return self.give_blueprint()

    def give_materials(self):
        """Distributes materials and a small Farm Currency reward"""
        user_profile = UserProfile.objects.get(user=self.user)

        MATERIALS = ["Wood", "Stone", "Metal", "Glass"]
        received_materials = random.choices(MATERIALS, k=3)  # Give 3 random materials
        farm_currency_bonus = Decimal(random.uniform(0.5, 2.0))  # Random currency

        user_profile.add_farm_currency(farm_currency_bonus, description="Crate Opening Reward")

        return {
            "materials": received_materials,
            "farm_currency_bonus": farm_currency_bonus
        }

    def give_blueprint(self):
        """Grants a random blueprint"""
        from apps.farm.models import Blueprint  # Import dynamically to avoid circular dependency
        blueprint = Blueprint.objects.order_by("?").first()  # Get random blueprint

        if blueprint:
            self.user.userprofile.blueprints.add(blueprint)  # Assuming a ManyToMany field exists

        return {"blueprint": blueprint.name if blueprint else None}