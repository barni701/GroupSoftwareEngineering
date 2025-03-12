# apps/farm/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from apps.farm.models import Building
from apps.crates.models import Item

class BuildingViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        # Create a sample blueprint item for potential upgrade (if needed)
        self.blueprint, _ = Item.objects.get_or_create(
            name="Test Blueprint", defaults={"item_type": "blueprint", "rarity": 1, "base_value": Decimal("5.00")}
        )
        # Create a test building
        self.building = Building.objects.create(
            user=self.user,
            name="Greenhouse",
            level=1,
            description="A simple greenhouse.",
            blueprint_required=self.blueprint  # Optional: if needed for upgrade
        )

    def test_building_list_view(self):
        url = reverse("building_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Greenhouse")

    def test_building_detail_view(self):
        url = reverse("building_detail", kwargs={"building_id": self.building.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Greenhouse")
        # Check that upgrade cost is displayed. Since level is 1, upgrade_cost should be base_cost.
        self.assertContains(response, "Upgrade Cost:")

    def test_upgrade_building_view(self):
        # Assume upgrade_building view upgrades the building when POSTed to.
        url = reverse("upgrade_building", kwargs={"building_id": self.building.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        # For example, if the view returns a JSON with new_level, check that the level increased.
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data.get("new_level"), self.building.level + 1)