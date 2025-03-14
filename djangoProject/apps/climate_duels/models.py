from django.db import models
from django.contrib.auth.models import User

class ClimateDuel(models.Model):
    """Stores an ongoing climate duel between two players."""
    player_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name="climate_duels_as_p1")
    player_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name="climate_duels_as_p2", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    player_one_budget = models.FloatField(default=100.0)  # Each player starts with 100 units of currency
    player_two_budget = models.FloatField(default=100.0)

    player_one_co2 = models.FloatField(default=100.0)  # Each player starts with 100 CO₂ units
    player_two_co2 = models.FloatField(default=100.0)

    player_one_gdp = models.FloatField(default=100.0)  # Economic stability
    player_two_gdp = models.FloatField(default=100.0)

    current_turn = models.IntegerField(default=1)

    def __str__(self):
        return f"Climate Duel: {self.player_one.username} vs {self.player_two.username or 'Waiting for Opponent'}"

class Policy(models.Model):
    """Stores climate policies that affect CO₂ and GDP."""
    name = models.CharField(max_length=100)
    co2_reduction = models.FloatField()  # How much CO₂ is reduced
    gdp_impact = models.FloatField()  # Negative value = economic cost
    cost = models.FloatField(default=10.0)  # New field: Default cost per policy

    def __str__(self):
        return self.name

class DuelTurn(models.Model):
    """Tracks each turn's decisions and results."""
    duel = models.ForeignKey(ClimateDuel, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    chosen_policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True, blank=True)
    co2_after_turn = models.FloatField()
    gdp_after_turn = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Turn {self.duel.current_turn} - {self.player.username}"
    
class PowerUp(models.Model):
    """Power-ups that players can use to gain advantages in a duel."""
    name = models.CharField(max_length=100)
    effect_type = models.CharField(max_length=50, choices=[
        ("co2_reduction", "CO₂ Reduction"),
        ("gdp_boost", "GDP Boost"),
        ("policy_boost", "Policy Effect x2"),
        ("block_opponent", "Block Opponent"),
    ])
    effect_value = models.FloatField()  # Numeric impact of the power-up
    description = models.TextField()
    
    def __str__(self):
        return self.name

class PlayerPowerUp(models.Model):
    """Tracks which power-ups each player owns."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    powerup = models.ForeignKey(PowerUp, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Players can collect multiple

    def __str__(self):
        return f"{self.user.username} - {self.powerup.name} x{self.quantity}"