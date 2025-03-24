from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.crates.models import Item  # Assuming seeds are stored as Items of a specific type
from apps.users.models import UserProfile

class GardenPlot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="garden_plots")
    name = models.CharField(max_length=100, default="Plot")
    created_at = models.DateTimeField(auto_now_add=True)
    # A plot can have one plant at a time; null means it's empty.
    current_plant = models.OneToOneField("GardenPlant", on_delete=models.SET_NULL, null=True, blank=True, related_name="plot")

    def __str__(self):
        return f"{self.user.username}'s {self.name}"

class GardenPlant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="garden_plants")
    seed = models.ForeignKey(Item, on_delete=models.CASCADE, help_text="Seed used for planting; should be an item of type 'seed'")
    planted_at = models.DateTimeField(default=timezone.now)
    growth_duration = models.DurationField(default=timedelta(hours=1), help_text="Time required for full growth")
    is_harvested = models.BooleanField(default=False)
    
    def time_until_harvest(self):
        """Returns the remaining time until the plant is ready to harvest."""
        end_time = self.planted_at + self.growth_duration
        remaining = end_time - timezone.now()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)

    def is_ready_to_harvest(self):
        """Returns True if the plant is ready to harvest."""
        return self.time_until_harvest() == timedelta(0)

    def is_fully_grown(self):
        """Returns True if the plant has finished growing but hasn't been harvested."""
        return self.is_ready_to_harvest() and not self.is_harvested

    def __str__(self):
        return f"{self.seed.name} planted by {self.user.username}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        profile = UserProfile.objects.get(user=self.user)

        if is_new:
            profile.total_garden_plants += 1
        if self.is_harvested:
            profile.harvested_plants += 1

        profile.save()

@property
def progress_percentage(self):
    """
    Calculate the growth progress percentage:
    ((total growth time - remaining time) / total growth time) * 100
    """
    total = self.growth_duration.total_seconds()
    remaining = self.time_until_harvest().total_seconds() if self.time_until_harvest() else 0
    if total <= 0:
        return 100
    progress = ((total - remaining) / total) * 100
    return int(progress)