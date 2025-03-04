import random
from decimal import Decimal

class CrateType:
    """Defines the contents and properties of a crate."""
    def __init__(self, name, price, currency, loot_pool, rarity_boost=1.0):
        self.name = name
        self.price = Decimal(price)
        self.currency = currency  # "main" or "farm"
        self.loot_pool = loot_pool  # Each tuple: (item_name, item_type, base_rarity, drop_rate)
        self.rarity_boost = rarity_boost

    '''def get_random_drop(self):
        """Returns a random item name based on weighted drop rates."""
        items, weights = zip(*[(loot[0], loot[3]) for loot in self.loot_pool])
        return random.choices(items, weights=weights, k=1)[0]
'''
    def get_random_loot(self):
        """Returns the full loot tuple based on weighted drop rates."""
        loot_choices = self.loot_pool
        weights = [loot[3] for loot in loot_choices]
        return random.choices(loot_choices, weights=weights, k=1)[0]

CRATE_TYPES = {
    "materials": CrateType(
        name="Materials Crate",
        price="10.00",
        currency="main",
        loot_pool=[
            ("Wood", "material", 1, 50),
            ("Stone", "material", 1, 20),
            ("Metal", "material", 2, 15),
            ("Glass", "material", 2, 5),
            ("Eco-Tokens", "currency", 2, 10, (1, 5)),
        ],
        rarity_boost=1.0
    ),
    "blueprint": CrateType(
        name="Blueprint Crate",
        price="15.00",
        currency="farm",
        loot_pool=[
            ("Farm Expansion", "blueprint", 2, 50),
            ("Solar Panels", "blueprint", 3, 30),
            ("Irrigation System", "blueprint", 4, 20),
        ],
        rarity_boost=1.2
    ),
    "special": CrateType(
        name="Special Crate",
        price="25.00",
        currency="main",
        loot_pool=[
            ("Golden Seeds", "special", 4, 5),
            ("Eco-Tokens", "currency", 3, 25, (10, 25)),
            ("Rare Metal", "special", 2, 70),
        ],
        rarity_boost=1.5
    ),
    "mystery": CrateType(
        name="Mystery Crate",
        price="30.00",
        currency="main",
        loot_pool=[
            ("Ancient Relic", "special", 4, 10),
            ("Mysterious Scroll", "special", 3, 40),
            ("Enchanted Gem", "special", 5, 50),
        ],
        rarity_boost=2.0
    ),
    "epic": CrateType(
        name="Epic Crate",
        price="50.00",
        currency="farm",
        loot_pool=[
            ("Dragon Scale", "special", 5, 10),
            ("Phoenix Feather", "special", 5, 20),
            ("Mystic Orb", "special", 4, 70),
        ],
        rarity_boost=2.5
    ),
    "legendary": CrateType(
        name="Legendary Crate",
        price="75.00",
        currency="main",
        loot_pool=[
            ("Excalibur", "special", 5, 2),
            ("Phoenix Feather", "special", 5, 3),
            ("Mystic Orb", "special", 4, 5),
            ("Ancient Scroll", "special", 3, 10),
            ("Dragon Scale", "special", 4, 5),
            ("Magic Potion", "consumable", 2, 15),
            ("Enchanted Gem", "special", 5, 4),
            ("Rusty Sword", "material", 1, 30),
            ("Legendary Armor", "special", 5, 1),
            ("Cursed Dagger", "special", 3, 8),
            ("Mystic Robe", "special", 4, 7),
            ("Arcane Book", "blueprint", 3, 12),
            ("Sapphire", "special", 3, 10),
            ("Ruby", "special", 4, 9),
            ("Emerald", "special", 4, 9),
            ("Obsidian Shard", "material", 2, 25),
            ("Crystal Ball", "special", 4, 6)
        ],
        rarity_boost=2.0
    ),
    "eco": CrateType(
        name="Eco Crate",
        price="20.00",
        currency="main",
        loot_pool=[
            ("Recycled Plastic", "material", 1, 40),
            ("Organic Compost", "material", 1, 30),
            ("Solar Panel", "blueprint", 2, 20),
            ("Sustainable Seed", "material", 2, 15),
            ("Eco Badge", "special", 3, 10),
            ("Carbon Credit", "currency", 4, 5, (40, 80)),
            ("Farm Voucher", "currency", 3, 8, (5, 30)),
            ("Green Token", "special", 5, 2)
        ],
        rarity_boost=1.3
    ),
    "renewable_energy": CrateType(
        name="Renewable Energy Crate",
        price="25.00",
        currency="main",
        loot_pool=[
            ("Solar Battery", "material", 2, 30),
            ("Wind Turbine Blueprint", "blueprint", 3, 25),
            ("Geothermal Circuit", "special", 4, 15),
            ("Energy Token", "currency", 2, 20, (10, 50)),
            ("Hydro Generator", "blueprint", 3, 10),
        ],
        rarity_boost=1.4
    ),
    "forest_guardian": CrateType(
        name="Forest Guardian Crate",
        price="35.00",
        currency="farm",
        loot_pool=[
            ("Ancient Sapling", "special", 5, 25),
            ("Animal Companion Blueprint", "blueprint", 4, 20),
            ("Moss Cubes", "material", 2, 15),
            ("Rainwater Collector", "blueprint", 3, 25),
            ("Forest Token", "currency", 3, 15, (50, 100)),
        ],
        rarity_boost=1.6
    ),
    "ocean_savior": CrateType(
        name="Ocean Savior Crate",
        price="30.00",
        currency="main",
        loot_pool=[
            ("Recycled Netting", "material", 1, 35),
            ("Coral Polyp", "special", 4, 25),
            ("Tide Turbine Blueprint", "blueprint", 3, 20),
            ("Plastic Credits", "currency", 4, 15, (20, 100)),
            ("Pearl of the Ocean", "special", 5, 5),
        ],
        rarity_boost=1.5
    ),
    "pollinator": CrateType(
        name="Pollinator Crate",
        price="18.00",
        currency="farm",
        loot_pool=[
            ("Beehive Blueprint", "blueprint", 2, 40),
            ("Rare Flower Seeds", "material", 3, 30),
            ("Royal Jelly", "special", 4, 15),
            ("Pollen Token", "currency", 2, 10, (5, 20)),
            ("Butterfly Companion", "special", 5, 5),
        ],
        rarity_boost=1.3
    ),
    "zero_waste": CrateType(
        name="Zero Waste Crate",
        price="22.00",
        currency="main",
        loot_pool=[
            ("Compostable Plastic", "material", 1, 35),
            ("Upcycled Fabric", "material", 2, 30),
            ("Zero-Waste Kit Blueprint", "blueprint", 3, 20),
            ("Recycling Voucher", "currency", 2, 10, (1, 10)),
            ("Eco Enzyme", "special", 3, 5),
        ],
        rarity_boost=1.2
    ),
    "climate_action": CrateType(
        name="Climate Action Crate",
        price="40.00",
        currency="farm",
        loot_pool=[
            ("Carbon Capture Unit Blueprint", "blueprint", 4, 25),
            ("Drought-Resistant Seeds", "material", 3, 30),
            ("Climate Token", "currency", 5, 25, (100, 200)),
            ("Weather Control Chip", "special", 5, 15),
            ("Climate Manifesto", "special", 1, 5),
        ],
        rarity_boost=1.8
    ),
}