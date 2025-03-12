# apps/farm/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.farm.models import Building

@receiver(post_save, sender=User)
def create_starting_buildings(sender, instance, created, **kwargs):
    if created:
        # Create default building: Basic Greenhouse
        Building.objects.create(
            user=instance,
            name="Basic Greenhouse",
            level=1,
            description="Your starter greenhouse for growing crops."
        )
        # Create another default building: Small Barn
        Building.objects.create(
            user=instance,
            name="Small Barn",
            level=1,
            description="A small barn to house your animals and store feed."
        )