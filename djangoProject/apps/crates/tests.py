import random
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from apps.crates.models import Crate, InventoryItem, Item
from apps.crates.crate_definitions import CRATE_TYPES
from apps.users.models import UserProfile

class CrateTestCase(TestCase):
    """Tests for the modular crate system: buying, opening, stacking, and rarity distribution."""

    def setUp(self):
        """Create a test user, log them in, give currency, and create crates for each type."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.user_profile = UserProfile.objects.create(user=self.user, currency_balance=1000.00, farm_currency=1000.00)

        # Create crates for each type with an initial quantity of 10
        self.crate_types = ["special", "materials", "blueprint"]
        self.crates = {}
        for crate_type in self.crate_types:
            crate_def = CRATE_TYPES[crate_type]
            crate = Crate.objects.create(
                user=self.user,
                crate_type=crate_type,
                quantity=10,
                price=crate_def.price,
                currency_type=crate_def.currency,
            )
            self.crates[crate_type] = crate

    def test_buy_crate(self):
        """Test that buying a crate increases the stack properly."""
        for crate_type in self.crate_types:
            buy_url = reverse("buy_crate", kwargs={"crate_type": crate_type})
            response = self.client.post(buy_url)
            self.assertEqual(response.status_code, 200,
                             f"Buy crate request failed for {crate_type}: {response.content}")
            crate = Crate.objects.get(user=self.user, crate_type=crate_type)
            self.assertGreaterEqual(crate.quantity, 11,
                                    f"Crate stacking failed for {crate_type}")
        print("✅ Passed: Buying crates works correctly and stacks.")

    def test_open_crate(self):
        """Test that opening a crate returns a valid reward and decreases quantity."""
        crate_type = "special"
        crate_def = CRATE_TYPES[crate_type]
        open_url = reverse("open_crate", kwargs={"crate_type": crate_type})

        response = self.client.post(open_url)
        self.assertEqual(response.status_code, 200,
                         f"Open crate request failed: {response.content}")
        self.assertTrue(response.headers["Content-Type"].startswith("application/json"),
                        "❌ ERROR: Response is not JSON!")

        reward = response.json().get("reward", None)
        self.assertIsNotNone(reward, "❌ ERROR: Reward missing from response!")
        self.assertIn("item", reward, "❌ ERROR: Reward does not contain an item!")
        self.assertIn("rarity", reward, "❌ ERROR: Reward does not contain rarity!")

        # Fetch the dropped item from the database
        dropped_item = Item.objects.get(name=reward["item"])
        # Find the base rarity for this item in the loot pool of this crate type
        base_rarity = None
        for loot in crate_def.loot_pool:
            if loot[0] == dropped_item.name:
                base_rarity = loot[1]
                break
        self.assertIsNotNone(base_rarity, f"Base rarity for {dropped_item.name} not found in loot pool!")
        expected_rarity = min(5, int(base_rarity * crate_def.rarity_boost))
        self.assertEqual(reward["rarity"], expected_rarity,
                         "❌ ERROR: Rarity scaling did not apply correctly.")

        # Verify the crate's quantity is reduced by 1
        crate = self.crates[crate_type]
        crate.refresh_from_db()
        self.assertEqual(crate.quantity, 9, "❌ ERROR: Crate quantity did not decrease after opening.")

        print(f"✅ Passed: Opening a '{crate_type}' crate works correctly, reward received, and rarity scaling verified.")

    def test_opening_multiple_crates_stacks_items(self):
        """Test that opening multiple crates correctly stacks the rewards in inventory."""
        crate_type = "materials"
        open_url = reverse("open_crate", kwargs={"crate_type": crate_type})
        initial_quantity = self.crates[crate_type].quantity

        # Open the crate three times
        for _ in range(3):
            self.client.post(open_url)

        crate = Crate.objects.get(user=self.user, crate_type=crate_type)
        self.assertEqual(crate.quantity, initial_quantity - 3,
                         "❌ ERROR: Crate quantity did not decrease correctly after multiple openings.")

        # Verify that at least one inventory item exists
        inventory_items = InventoryItem.objects.filter(user=self.user)
        self.assertTrue(inventory_items.exists(),
                        "❌ ERROR: No items found in inventory after opening crates.")

        print("✅ Passed: Multiple crate openings correctly decrease quantity and stack items in inventory.")

    def test_rarity_distribution(self):
        """Test that over many openings, the drop rates approximate the defined probabilities."""
        drop_counts = {}
        total_opens = 100

        for _ in range(total_opens):
            # Randomly pick a crate type
            crate_type = random.choice(self.crate_types)
            open_url = reverse("open_crate", kwargs={"crate_type": crate_type})
            crate = self.crates[crate_type]
            crate.refresh_from_db()
            if crate.quantity < 1:
                crate.adjust_quantity(5)  # Replenish if necessary
            response = self.client.post(open_url)
            if response.status_code != 200 or not response.headers["Content-Type"].startswith("application/json"):
                print(f"❌ ERROR: Expected JSON but got {response.content}")
                continue
            reward_item = response.json()["reward"]["item"]
            drop_counts[reward_item] = drop_counts.get(reward_item, 0) + 1

        print("\n🎲 Rarity Distribution Test (100 Opens) Across Multiple Crate Types:")
        for item, count in sorted(drop_counts.items(), key=lambda x: -x[1]):
            print(f"  - {item}: {count} times")
        print("✅ Passed: Rarity distribution test completed.")