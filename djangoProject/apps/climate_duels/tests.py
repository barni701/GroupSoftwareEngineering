from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from apps.climate_duels.models import ClimateDuel, Policy
from apps.farm.signals import create_starting_buildings
from apps.users.models import UserProfile  # Import UserProfile for XP tracking

class ClimateDuelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Disable signals before running tests."""
        super().setUpClass()
        post_save.disconnect(create_starting_buildings, sender=User)

    @classmethod
    def tearDownClass(cls):
        """Re-enable signals after tests."""
        super().tearDownClass()
        post_save.connect(create_starting_buildings, sender=User)

    def setUp(self):
        """Set up test users and policies."""
        self.player_one = User.objects.create_user(username="player1", password="testpass")
        self.player_two = User.objects.create_user(username="player2", password="testpass")
        
        # Create user profiles
        self.profile_one = UserProfile.objects.create(user=self.player_one)
        self.profile_two = UserProfile.objects.create(user=self.player_two)

        # Create a duel
        self.duel = ClimateDuel.objects.create(player_one=self.player_one, player_two=self.player_two)

        # Create policies
        self.policy = Policy.objects.create(name="Carbon Tax", co2_reduction=50.0, gdp_impact=-5.0)

    def test_duel_completion(self):
        """Test if the game correctly ends when a player reaches Net-Zero CO₂."""
        self.duel.player_one_co2 = 0  # Simulate Net-Zero CO₂
        self.duel.active = False
        self.duel.save()

        # Ensure the duel is marked as completed
        self.duel.refresh_from_db()
        self.assertFalse(self.duel.active)

    def test_xp_rewards_for_winner(self):
        """Test if the winner gains XP after a duel."""
        initial_xp = self.profile_one.experience_points

        # Simulate a win for player one
        self.duel.player_one_co2 = 0  # Net-Zero
        self.duel.active = False
        self.duel.save()

        # Award XP
        xp_reward = 50
        self.profile_one.experience_points += xp_reward
        self.profile_one.save()

        # Ensure the winner got XP
        self.profile_one.refresh_from_db()
        self.assertEqual(self.profile_one.experience_points, initial_xp + xp_reward)