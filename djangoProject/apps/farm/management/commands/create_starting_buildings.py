# apps/farm/management/commands/create_starting_buildings.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.farm.models import Building

class Command(BaseCommand):
    help = "Creates starting buildings for existing users without buildings."

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            # Check if the user already has any buildings.
            if not user.buildings.exists():
                Building.objects.create(
                    user=user,
                    name="Basic Greenhouse",
                    level=1,
                    description="Your starter greenhouse for growing crops."
                )
                Building.objects.create(
                    user=user,
                    name="Small Barn",
                    level=1,
                    description="A small barn to house your animals and store feed."
                )
                self.stdout.write(self.style.SUCCESS(f"Created starting buildings for user {user.username}"))
            else:
                self.stdout.write(f"User {user.username} already has buildings. Skipping.")
        self.stdout.write("Completed creating starting buildings for existing users!")