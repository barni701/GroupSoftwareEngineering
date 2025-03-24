from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BattlePass(models.Model):
    name = models.CharField(max_length=255)
    season_number = models.IntegerField(unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_tiers = models.IntegerField(default=50)

    def is_active(self):
        return self.start_date <= timezone.now() <= self.end_date

    def __str__(self):
        return f"Battle Pass Season {self.season_number}"

class BattlePassTier(models.Model):
    battle_pass = models.ForeignKey(BattlePass, on_delete=models.CASCADE)
    tier_level = models.IntegerField()
    reward_name = models.CharField(max_length=255)
    reward_type = models.CharField(max_length=50, choices=[
        ('currency', 'Currency'),
        ('item', 'Item'),
        ('badge', 'Badge')
    ])
    reward_value = models.IntegerField()  # Currency amount or item ID
    is_premium = models.BooleanField(default=False)  # ✅ New field for premium rewards

    def __str__(self):
        tier_type = "Premium" if self.is_premium else "Free"
        return f"Tier {self.tier_level} - {self.reward_name} ({tier_type})"

class UserBattlePass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    battle_pass = models.ForeignKey("BattlePass", on_delete=models.CASCADE)
    current_tier = models.IntegerField(default=0)
    progress_points = models.IntegerField(default=0)
    has_premium = models.BooleanField(default=False)

    def progress_to_next_tier(self):
        """Allow multiple level-ups and retain excess XP."""
        from .views import grant_reward  # ✅ Import locally to avoid circular import

        required_points_per_tier = 100

        while self.progress_points >= required_points_per_tier:
            self.progress_points -= required_points_per_tier  # subtract exactly what’s needed
            self.current_tier += 1

            free_reward = BattlePassTier.objects.filter(
                battle_pass=self.battle_pass,
                tier_level=self.current_tier,
                is_premium=False
            ).first()

            premium_reward = BattlePassTier.objects.filter(
                battle_pass=self.battle_pass,
                tier_level=self.current_tier,
                is_premium=True
            ).first()

            if free_reward:
                grant_reward(self.user, free_reward)

            if self.has_premium and premium_reward:
                grant_reward(self.user, premium_reward)

        self.save()
    
    @property
    def progress_percent(self):
        """Calculate the percentage progress toward the next tier."""
        required_points_per_tier = 100
        return (self.progress_points % required_points_per_tier)  # Ensure it's between 0 and 99