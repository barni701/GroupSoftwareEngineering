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

    def get_random_loot(self):
        """Returns the full loot tuple based on weighted drop rates."""
        loot_choices = self.loot_pool
        weights = [loot[3] for loot in loot_choices]
        return random.choices(loot_choices, weights=weights, k=1)[0]

CRATE_TYPES = {
    "materials": CrateType(
        name="Materials Crate",
        price="15.00",
        currency="main",
        loot_pool=[
            # Common materials (appear in multiple crates)
            ("Wood", "material", 1, 25),
            ("Stone", "material", 1, 30),
            ("Metal", "material", 2, 20),
            ("Glass", "material", 2, 15),
            ("Basic Electronics", "material", 2, 15),
            ("Plastic", "material", 1, 35),
            
            # Specialty materials
            ("Reinforced Glass", "material", 3, 10),
            ("Copper Wiring", "material", 2, 20),
            ("Eco-Concrete", "material", 2, 15)
        ],
        rarity_boost=1.1
    ),

    "advanced_materials": CrateType(
        name="Advanced Materials Crate",
        price="45.00",
        currency="main",
        loot_pool=[
            # Shared basic materials
            ("Metal", "material", 2, 25),
            ("Copper Wiring", "material", 2, 20),
            
            # Advanced electronics
            ("Advanced Electronics", "material", 4, 15),
            ("Carbon Fiber", "material", 3, 20),
            ("Nano-Silica", "material", 4, 10),
            ("Graphene Sheets", "material", 5, 5),
            
            # Cross-crate materials
            ("Reinforced Glass", "material", 3, 15)
        ],
        rarity_boost=1.4
    ),

    "eco_tech": CrateType(
        name="Eco-Tech Crate",
        price="35.00",
        currency="farm",
        loot_pool=[
            # Electronics at different tiers
            ("Basic Electronics", "material", 2, 30),
            ("Advanced Electronics", "material", 4, 10),
            
            # Shared construction materials
            ("Eco-Concrete", "material", 2, 25),
            ("Recycled Plastic", "material", 1, 40),
            
            # Specialty items
            ("Solar Cells", "material", 3, 20),
            ("Biofuel Catalyst", "material", 4, 15)
        ],
        rarity_boost=1.3
    ),

    "industrial": CrateType(
        name="Industrial Crate",
        price="50.00",
        currency="main",
        loot_pool=[
            # Core materials
            ("Steel Beams", "material", 3, 30),
            ("Industrial Plastic", "material", 2, 40),
            
            # Electronics progression
            ("Basic Electronics", "material", 2, 25),
            ("Advanced Electronics", "material", 4, 15),
            
            # Shared advanced materials
            ("Carbon Fiber", "material", 3, 20),
            ("Nano-Silica", "material", 4, 10)
        ],
        rarity_boost=1.5
    ),

    "green_construction": CrateType(
        name="Green Construction Crate",
        price="40.00",
        currency="farm",
        loot_pool=[
            # Base materials
            ("Wood", "material", 1, 30),
            ("Stone", "material", 1, 25),
            
            # Electronics for smart systems
            ("Basic Electronics", "material", 2, 20),
            
            # Specialized materials
            ("Bamboo Composite", "material", 3, 25),
            ("Mycelium Insulation", "material", 4, 15),
            ("Recycled Steel", "material", 2, 30)
        ],
        rarity_boost=1.2
    ),

    "high_tech": CrateType(
        name="High-Tech Crate",
        price="75.00",
        currency="main",
        loot_pool=[
            # Electronics focus
            ("Advanced Electronics", "material", 4, 40),
            ("Quantum Chips", "material", 5, 15),
            
            # Shared materials
            ("Graphene Sheets", "material", 5, 10),
            ("Carbon Fiber", "material", 3, 25),
            
            # Specialty components
            ("Neural Processors", "material", 5, 5),
            ("Optical Sensors", "material", 4, 20)
        ],
        rarity_boost=1.8
    ),

    # Existing crates updated with material overlap
    "blueprint": CrateType(
        name="Blueprint Crate",
        price="25.00",
        currency="farm",
        loot_pool=[
            ("Smart Irrigation", "blueprint", 3, 25),
            ("Solar Array", "blueprint", 2, 30),
            ("Wind Turbine", "blueprint", 3, 20),
            ("Advanced Electronics", "material", 4, 15),  # Added material
            ("Eco-Concrete", "material", 2, 10)  # Shared material
        ],
        rarity_boost=1.4
    ),

    "epic": CrateType(
        name="Epic Crate",
        price="85.00",
        currency="main",
        loot_pool=[
            ("Nanotech Solar", "special", 5, 15),
            ("Plasma Converter", "special", 5, 10),
            ("Advanced Electronics", "material", 4, 30),  # Increased presence
            ("Graphene Sheets", "material", 5, 20),
            ("Quantum Chips", "material", 5, 15)
        ],
        rarity_boost=2.2
    ),
    "rare_blueprint": CrateType(
        name="Rare Blueprint Crate",
        price="40.00",
        currency="farm",
        loot_pool=[
            ("Precision Seeder", "blueprint", 3, 20),
            ("Advanced Irrigation System", "blueprint", 4, 15),
            ("High-Efficiency Greenhouse", "blueprint", 4, 10),
            ("Automated Crop Monitor", "blueprint", 3, 25),
            ("Sustainable Energy Optimizer", "blueprint", 4, 10),
        ],
        rarity_boost=1.3
    ),
    "special": CrateType(
        name="Special Crate",
        price="25.00",
        currency="main",
        loot_pool=[
            ("Golden Seeds", "special", 4, 5),
            ("Eco-Tokens", "currency", 3, 25, (10, 25)),
            ("Rare Metal", "material", 2, 70),
            ("Drill Components", "material", 3, 20),
            ("Tools", "material", 2, 30),
            ("Waterproofing", "material", 2, 25),
            ("Drainage", "material", 2, 15),
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
    "legendary": CrateType(
        name="Legendary Crate",
        price="75.00",
        currency="main",
        loot_pool=[
            ("Gaia's Embrace", "special", 5, 2),
            ("Verdant Orb", "special", 4, 5),
            ("Ancient Tree Scroll", "special", 3, 10),
            ("Nature's Codex", "blueprint", 3, 12),
            ("Emerald Leaf", "special", 3, 10),
            ("Ruby Blossom", "special", 4, 9),
            ("Sapphire Dew", "material", 4, 9),
            ("Obsidian Bark", "material", 2, 25),
            ("Crystal Sap", "material", 4, 6)
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
            ("Carbon Credit", "currency", 4, 5, (40,80)),
            ("Farm Voucher", "currency", 3, 8, (5,30)),
            ("Green Token", "special", 5, 2)
        ],
        rarity_boost=1.3
    ),
    "advanced_materials": CrateType(
        name="Advanced Materials Crate",
        price="30.00",
        currency="main",
        loot_pool=[
            ("Titanium", "material", 3, 30),
            ("Carbon Fiber", "material", 4, 20),
            ("Composite Alloy", "material", 3, 25),
            ("Nano Coating", "material", 4, 15),
            ("Advanced Electronics", "material", 3, 20),
        ],
        rarity_boost=1.1
    ),
    "farm_currency": CrateType(
        name="Farm Currency Crate",
        price="25.00",
        currency="farm",
        loot_pool=[
            ("Organic Compost", "material", 1, 30),
            ("Solar Panel", "blueprint", 2, 20),
            ("Eco Badge", "special", 3, 15),
            ("Farm Voucher", "special", 3, 15)
        ],
        rarity_boost=1.0
    ),
    "plant_seed": CrateType(
        name="Plant Seed Crate",
        price="5.00",
        currency="main",
        loot_pool=[
            ("Sunflower Seeds", "seed", 1, 40),
            ("Pumpkin Seeds", "seed", 1, 30),
            ("Bean Seeds", "seed", 1, 20),
            ("Corn Seeds", "seed", 1, 10)
        ],
        rarity_boost=1.0
    ),

"rare_seed": CrateType(
    name="Rare Herb Crate",
    price="15.00",
    currency="main",
    loot_pool=[
        ("Lavender Seeds", "seed", 2, 35),
        ("Rosemary Seeds", "seed", 2, 30),
        ("Mint Seeds", "seed", 2, 25),
        ("Thyme Seeds", "seed", 2, 10)
    ],
    rarity_boost=1.2
),

"exotic_seed": CrateType(
    name="Exotic Flora Crate",
    price="30.00",
    currency="main",
    loot_pool=[
        ("Orchid Bulbs", "seed", 3, 40),
        ("Bamboo Shoots", "seed", 3, 30),
        ("Lotus Pods", "seed", 3, 20),
        ("Venus Flytrap Spores", "seed", 3, 10)
    ],
    rarity_boost=1.5
),

"mythical_seed": CrateType(
    name="Mythical Garden Crate",
    price="60.00",
    currency="main",
    loot_pool=[
        ("Dragonfruit Seeds", "seed", 4, 30),
        ("Mandrake Roots", "seed", 4, 30),
        ("Moonflower Seeds", "seed", 4, 25),
        ("Phoenix Fern Spores", "seed", 4, 15)
    ],
    rarity_boost=2.0
),

"legendary_seed": CrateType(
    name="Legendary Botanical Crate",
    price="100.00",
    currency="main",
    loot_pool=[
        ("Golden Apple Sapling", "seed", 5, 25),
        ("Crystal Berry Seeds", "seed", 5, 25),
        ("Eternal Oak Acorn", "seed", 5, 30),
        ("Shadow Vine Spores", "seed", 5, 20)
    ],
    rarity_boost=3.0
)
}