import random
from decimal import Decimal

class CrateType:
    """Defines the contents and properties of a crate."""
    def __init__(self, name, price, currency, loot_pool, rarity_boost=1.0):
        self.name = name
        self.price = Decimal(price)
        self.currency = currency  # "main" or "farm"
        self.loot_pool = loot_pool  # Each tuple: (item_name, base_rarity, drop_rate)
        self.rarity_boost = rarity_boost

    def get_random_drop(self):
        """Returns a random item name based on weighted drop rates."""
        items, weights = zip(*[(item[0], item[2]) for item in self.loot_pool])
        return random.choices(items, weights=weights, k=1)[0]

CRATE_TYPES = {
    "materials": CrateType(
        name="Materials Crate",
        price="10.00",
        currency="main",
        loot_pool=[
            ("Wood", 1, 60),
            ("Stone", 1, 20),
            ("Metal", 2, 15),
            ("Glass", 2, 5),
        ],
        rarity_boost=1.0
    ),
    "blueprint": CrateType(
        name="Blueprint Crate",
        price="15.00",
        currency="farm",
        loot_pool=[
            ("Farm Expansion", 2, 50),
            ("Solar Panels", 3, 30),
            ("Irrigation System", 4, 20),
        ],
        rarity_boost=1.2
    ),
    "special": CrateType(
        name="Special Crate",
        price="25.00",
        currency="main",
        loot_pool=[
            ("Golden Seeds", 4, 5),
            ("Eco-Tokens", 3, 25),
            ("Rare Metal", 2, 70),
        ],
        rarity_boost=1.5
    ),
    "mystery": CrateType(
        name="Mystery Crate",
        price="30.00",
        currency="main",
        loot_pool=[
            ("Ancient Relic", 4, 10),
            ("Mysterious Scroll", 3, 40),
            ("Enchanted Gem", 5, 50),
        ],
        rarity_boost=2.0
    ),
    "epic": CrateType(
        name="Epic Crate",
        price="50.00",
        currency="farm",
        loot_pool=[
            ("Dragon Scale", 5, 10),
            ("Phoenix Feather", 5, 20),
            ("Mystic Orb", 4, 70),
        ],
        rarity_boost=2.5
    ),
}