from django.db import models
from apps.crates.models import Item
from django.contrib.auth.models import User
from decimal import Decimal

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