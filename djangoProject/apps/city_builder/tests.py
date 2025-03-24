from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal

from apps.crates.models import InventoryItem, Item
from .models import City, BuildingTemplate, CityBuilding

class CityBuilderTestCase(TestCase):
    def setUp(self):
        # Create a test user and a city for them
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.city = City.objects.create(user=self.user, funds=Decimal("500.00"))
        # Create a building template
        self.template = BuildingTemplate.objects.create(
            name="Solar Panel",
            description="Generates renewable energy.",
            base_cost=Decimal("100.00"),
            resource_requirements={"glass": 20, "metal": 10},
            sustainability_bonus=Decimal("5.00"),
            upgrade_multiplier=Decimal("1.5"),
        )
        # Log the user in
        self.client.login(username="testuser", password="testpass")
    
    def test_city_dashboard(self):
        url = reverse("city_dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.city.name)
    
    def test_building_catalog(self):
        url = reverse("building_catalog")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.template.name)
    
    def test_construct_building(self):
        url = reverse("construct_building", args=[self.template.id])
        # Post coordinates that are not occupied
        data = {"x": 1, "y": 1}
        response = self.client.post(url, data)
        # Expect a redirect to the dashboard on success
        self.assertEqual(response.status_code, 302)
        # Verify that a CityBuilding was created
        building = CityBuilding.objects.get(city=self.city, x=1, y=1)
        self.assertEqual(building.template, self.template)
        # Verify that funds were deducted (100.00 from 500.00)
        self.city.refresh_from_db()
        self.assertEqual(self.city.funds, Decimal("400.00"))
    
    def test_upgrade_building(self):
        # Create inventory items for the required materials ("glass" and "metal")
        glass_item, _ = Item.objects.get_or_create(
            name="glass", 
            defaults={"item_type": "material", "rarity": 1, "base_value": Decimal("1.00")}
        )
        metal_item, _ = Item.objects.get_or_create(
            name="metal", 
            defaults={"item_type": "material", "rarity": 1, "base_value": Decimal("1.00")}
        )
        # Provide enough materials so that the upgrade requirements (glass:20, metal:10) are met.
        InventoryItem.objects.create(user=self.user, item=glass_item, quantity=50)
        InventoryItem.objects.create(user=self.user, item=metal_item, quantity=50)

        building = CityBuilding.objects.create(
            city=self.city,
            template=self.template,
            x=2,
            y=2,
            upgrade_level=1
        )
        upgrade_cost = self.template.get_upgrade_cost(building.upgrade_level)
        url = reverse("upgrade_building", args=[building.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        building.refresh_from_db()
        self.assertEqual(building.upgrade_level, 2)
        self.city.refresh_from_db()
        self.assertEqual(self.city.funds, Decimal("500.00") - upgrade_cost)

    def test_upgrade_building_materials(self):
        building = CityBuilding.objects.create(
            city=self.city,
            template=self.template,
            x=2,
            y=2,
            upgrade_level=1
        )
        # Create inventory items for "glass" and "metal", as required.
        glass_item, _ = Item.objects.get_or_create(
            name="glass", 
            defaults={"item_type": "material", "rarity": 1, "base_value": Decimal("1.00")}
        )
        metal_item, _ = Item.objects.get_or_create(
            name="metal", 
            defaults={"item_type": "material", "rarity": 1, "base_value": Decimal("1.00")}
        )
        InventoryItem.objects.create(user=self.user, item=glass_item, quantity=200)
        InventoryItem.objects.create(user=self.user, item=metal_item, quantity=100)
        
        success, cost, missing = building.upgrade()
        self.assertTrue(success)
        building.refresh_from_db()
        self.assertEqual(building.upgrade_level, 2)