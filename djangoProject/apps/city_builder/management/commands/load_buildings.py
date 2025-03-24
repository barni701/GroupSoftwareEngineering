from django.core.management.base import BaseCommand
from apps.city_builder.models import BuildingTemplate
from apps.city_builder.building_definitions import BUILDING_DEFINITIONS

class Command(BaseCommand):
    help = "Load or update building definitions"

    def handle(self, *args, **options):
        for key, defn in BUILDING_DEFINITIONS.items():
            template, created = BuildingTemplate.objects.update_or_create(
                name=defn.name,
                defaults={
                    "description": defn.description,
                    "base_cost": defn.base_cost,
                    "resource_requirements": defn.resource_requirements,
                    "sustainability_bonus": defn.sustainability_bonus,
                    "upgrade_multiplier": defn.upgrade_multiplier,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created template: {defn.name}"))
            else:
                self.stdout.write(f"Updated template: {defn.name}")
        self.stdout.write(self.style.SUCCESS("All building definitions have been loaded."))