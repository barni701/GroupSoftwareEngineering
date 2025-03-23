from django.db import models
from apps.crates.models import Item
from django.contrib.auth.models import User
from decimal import Decimal
from apps.users.models import UserProfile

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    result_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="crafted_by")
    result_quantity = models.PositiveIntegerField(default=1)
    # ManyToMany relation with Item via RecipeIngredient
    ingredients = models.ManyToManyField(Item, through='RecipeIngredient')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity} x {self.ingredient.name} for {self.recipe.name}"

class CraftingLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    rare = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update user profile stats
        profile = UserProfile.objects.get(user=self.user)
        profile.total_items_crafted += 1
        if self.rare:
            profile.rare_items_crafted += 1

        # Optionally update most crafted item
        from django.db.models import Count
        most_common = (
            CraftingLog.objects.filter(user=self.user)
            .values("recipe__name")
            .annotate(total=Count("id"))
            .order_by("-total")
            .first()
        )
        if most_common:
            profile.most_crafted_item = most_common["recipe__name"]

        profile.save()