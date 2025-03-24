from django.core.management.base import BaseCommand
from apps.battlepass.models import BattlePass, BattlePassTier
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Generate placeholder Battle Pass rewards"

    def handle(self, *args, **kwargs):
        # Ensure a Battle Pass exists
        battle_pass, created = BattlePass.objects.get_or_create(
            season_number=1,
            defaults={
                "name": "Eco Warrior Season 1",
                "start_date": timezone.now(),
                "end_date": timezone.now() + timedelta(days=30),
                "max_tiers": 50
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new Battle Pass: {battle_pass.name}"))
        else:
            self.stdout.write(self.style.WARNING(f"Using existing Battle Pass: {battle_pass.name}"))

        # Placeholder rewards
        free_rewards = [
            ("100 Coins", "currency", 100),
            ("Basic Lootbox", "item", 1),
            ("Eco Badge", "badge", 1),
            ("250 Coins", "currency", 250),
            ("Green Warrior Title", "badge", 1),
            ("500 Coins", "currency", 500),
        ]
        premium_rewards = [
            ("300 Coins", "currency", 300),
            ("Premium Lootbox", "item", 2),
            ("Rare Eco Badge", "badge", 1),
            ("750 Coins", "currency", 750),
            ("Exclusive Green Skin", "item", 3),
            ("1000 Coins", "currency", 1000),
        ]

        # Generate tiers (1-50)
        free_tiers = []
        premium_tiers = []

        for tier_level in range(1, 51):
            free_reward_data = free_rewards[tier_level % len(free_rewards)]
            premium_reward_data = premium_rewards[tier_level % len(premium_rewards)]

            free_tiers.append(BattlePassTier(
                battle_pass=battle_pass,
                tier_level=tier_level,
                reward_name=free_reward_data[0],
                reward_type=free_reward_data[1],
                reward_value=free_reward_data[2],
                is_premium=False
            ))

            premium_tiers.append(BattlePassTier(
                battle_pass=battle_pass,
                tier_level=tier_level,
                reward_name=premium_reward_data[0],
                reward_type=premium_reward_data[1],
                reward_value=premium_reward_data[2],
                is_premium=True
            ))

        # Bulk create the rewards
        BattlePassTier.objects.bulk_create(free_tiers)
        BattlePassTier.objects.bulk_create(premium_tiers)

        self.stdout.write(self.style.SUCCESS("Battle Pass rewards generated successfully!"))