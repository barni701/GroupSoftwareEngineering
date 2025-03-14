from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from apps.garden.models import GardenPlot, GardenPlant
from apps.crates.models import Item, InventoryItem

class GardenAppTestCase(TestCase):
    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        
        # Create a garden plot for the user
        self.plot = GardenPlot.objects.create(user=self.user, name="Test Plot")
        
        # Create a seed item (make sure "seed" is in your ITEM_TYPES in Item model)
        self.seed_item, _ = Item.objects.get_or_create(
            name="Test Seed",
            defaults={
                "item_type": "seed",
                "rarity": 1,
                "base_value": 1.00,
                "description": "A test seed for planting."
            }
        )
        
        # Create an inventory item for the seed with a starting quantity of 5
        self.inv_item = InventoryItem.objects.create(user=self.user, item=self.seed_item, quantity=5)

    def test_garden_dashboard_view(self):
        url = reverse("garden_dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Garden Plots")
    
    def test_available_seeds_view(self):
        # Access available seeds view for a specific plot
        url = reverse("available_seeds", args=[self.plot.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Seed")
    
    def test_plant_seed(self):
        # Plant a seed in the empty plot
        url = reverse("plant_seed", args=[self.plot.id, self.seed_item.id])
        response = self.client.post(url)
        # Expect a redirect (HTTP 302) after successful planting
        self.assertEqual(response.status_code, 302)
        
        # Reload the plot and ensure current_plant is set
        self.plot.refresh_from_db()
        self.assertIsNotNone(self.plot.current_plant)
        
        # Ensure that the inventory quantity is reduced by 1 (from 5 to 4)
        self.inv_item.refresh_from_db()
        self.assertEqual(self.inv_item.quantity, 4)
    
    def test_harvest_crop(self):
        # First, plant a seed
        plant_url = reverse("plant_seed", args=[self.plot.id, self.seed_item.id])
        self.client.post(plant_url)
        self.plot.refresh_from_db()
        plant = self.plot.current_plant
        
        # Force the plant to be ready for harvest by setting a zero growth duration
        plant.growth_duration = timedelta(seconds=0)
        plant.save()
        
        # Harvest the crop
        harvest_url = reverse("harvest_crop", args=[plant.id])
        response = self.client.post(harvest_url)
        self.assertEqual(response.status_code, 302)
        
        # Ensure that the plot is now empty
        self.plot.refresh_from_db()
        self.assertIsNone(self.plot.current_plant)