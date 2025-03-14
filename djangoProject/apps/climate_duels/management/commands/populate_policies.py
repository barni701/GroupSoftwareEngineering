from django.core.management.base import BaseCommand
from apps.climate_duels.models import Policy

class Command(BaseCommand):
    help = "Populates the database with predefined climate policies"

    def handle(self, *args, **kwargs):
        policies = [
            {"name": "Carbon Tax", "co2_reduction": 5.0, "gdp_impact": -2.0, "cost": 10.0},
            {"name": "Solar Investment", "co2_reduction": 3.0, "gdp_impact": -1.0, "cost": 7.0},
            {"name": "Ban Fossil Fuels", "co2_reduction": 20.0, "gdp_impact": -10.0, "cost": 25.0},
            {"name": "Reforestation Program", "co2_reduction": 4.0, "gdp_impact": -1.5, "cost": 8.0},
            {"name": "Public Transport Expansion", "co2_reduction": 6.0, "gdp_impact": -3.0, "cost": 12.0},
            {"name": "Nuclear Power Incentives", "co2_reduction": 10.0, "gdp_impact": -4.0, "cost": 15.0},
            {"name": "Wind Energy Support", "co2_reduction": 8.0, "gdp_impact": -3.5, "cost": 13.0},
            {"name": "Energy Efficiency Programs", "co2_reduction": 7.0, "gdp_impact": -2.5, "cost": 9.0},
        ]

        for policy in policies:
            Policy.objects.update_or_create(name=policy["name"], defaults=policy)

        self.stdout.write(self.style.SUCCESS("Successfully populated climate policies with cost field."))
