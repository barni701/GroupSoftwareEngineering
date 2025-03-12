# apps/crafting/recipe_definitions.py

class RecipeDefinition:
    """
    A lightweight definition for a crafting recipe.
    This definition contains:
      - name: Name of the recipe.
      - result_item: The name of the item produced.
      - result_quantity: How many units are produced.
      - ingredients: A list of tuples; each tuple is (item_name, required_quantity).
      - description: Optional description of the recipe.
      - item_type: The type/category for the resulting item (e.g., blueprint, consumable, special).
      - rarity: The base rarity of the resulting item.
      - base_value: The base monetary (or in-game) value of the item.
    """
    def __init__(self, name, result_item, result_quantity, ingredients, description="", item_type=None, rarity=None, base_value=None):
        self.name = name
        self.result_item = result_item
        self.result_quantity = result_quantity
        self.ingredients = ingredients  # List of tuples: (item_name, quantity)
        self.description = description
        self.item_type = item_type
        self.rarity = rarity
        self.base_value = base_value

    def __str__(self):
        return f"{self.name}: produces {self.result_quantity} x {self.result_item}"

RECIPE_DEFINITIONS = {
    "eco_fertilizer": RecipeDefinition(
        name="Eco Fertilizer Recipe",
        result_item="Eco Fertilizer",
        result_quantity=2,
        ingredients=[
            ("Recycled Plastic", 3),
            ("Organic Compost", 2),
        ],
        description="Craft eco fertilizer using recycled plastic and organic compost.",
        item_type="consumable",
        rarity=3,
        base_value=5.00
    ),
    "solar_panel_upgrade": RecipeDefinition(
        name="Solar Panel Upgrade Recipe",
        result_item="Premium Solar Panel",
        result_quantity=1,
        ingredients=[
            ("Solar Panel", 1),
            ("Eco Badge", 1),
        ],
        description="Upgrade your solar panel by combining it with an Eco Badge.",
        item_type="blueprint",
        rarity=3,
        base_value=15.00
    ),
    "green_energy_certificate": RecipeDefinition(
        name="Green Energy Certificate Recipe",
        result_item="Green Energy Certificate",
        result_quantity=1,
        ingredients=[
            ("Farm Voucher", 2),
            ("Carbon Credit", 1),
        ],
        description="Combine a farm voucher with a carbon credit to create a certificate for green energy investment.",
        item_type="special",
        rarity=4,
        base_value=20.00
    ),
    "advanced_greenhouse_blueprint": RecipeDefinition(
        name="Advanced Greenhouse Blueprint",
        result_item="Advanced Greenhouse",
        result_quantity=1,
        ingredients=[
            ("Glass", 20),
            ("Composite Alloy", 10),
            ("Organic Compost", 15),
            ("Solar Panel", 5),
        ],
        description="A blueprint to build a state-of-the-art greenhouse that maximizes crop yield.",
        item_type="blueprint",
        rarity=5,
        base_value=50.00
    ),
    "eco_irrigation_system_blueprint": RecipeDefinition(
        name="Eco Irrigation System Blueprint",
        result_item="Eco Irrigation System",
        result_quantity=1,
        ingredients=[
            ("Recycled Plastic", 30),
            ("Organic Compost", 10),
            ("Carbon Fiber", 5),
        ],
        description="A blueprint for an efficient irrigation system that uses recycled materials to conserve water.",
        item_type="blueprint",
        rarity=4,
        base_value=40.00
    ),
    "sustainable_energy_blueprint": RecipeDefinition(
        name="Sustainable Energy Blueprint",
        result_item="Sustainable Energy System",
        result_quantity=1,
        ingredients=[
            ("Solar Panel", 10),
            ("Eco Badge", 3),
            ("Carbon Credit", 2),
        ],
        description="A blueprint for an energy system that harnesses sustainable power sources for your farm.",
        item_type="blueprint",
        rarity=5,
        base_value=60.00
    ),
    "solar_farm_blueprint": RecipeDefinition(
        name="Solar Farm Blueprint",
        result_item="Solar Farm",
        result_quantity=1,
        ingredients=[
            ("Premium Solar Panel", 5),
            ("Composite Alloy", 10),
            ("Carbon Fiber", 5)
        ],
        description="Large-scale solar installation blueprint for maximum energy production.",
        item_type="blueprint",
        rarity=5,
        base_value=75.00
    ),
    "eco_compost_accelerator": RecipeDefinition(
        name="Eco Compost Accelerator",
        result_item="Eco Compost Accelerator",
        result_quantity=3,
        ingredients=[
            ("Organic Compost", 5),
            ("Eco Fertilizer", 2),
            ("Eco Catalyst", 1)
        ],
        description="Speeds up composting process using eco-friendly catalysts.",
        item_type="consumable",
        rarity=4,
        base_value=25.00
    ),
    "vertical_farm_blueprint": RecipeDefinition(
        name="Vertical Farming Blueprint",
        result_item="Vertical Farming Unit",
        result_quantity=1,
        ingredients=[
            ("Advanced Greenhouse", 1),
            ("Eco Irrigation System", 1),
            ("Composite Alloy", 20)
        ],
        description="Space-efficient vertical farm with automated growing systems.",
        item_type="blueprint",
        rarity=5,
        base_value=85.00
    ),
    "carbon_neutral_certificate": RecipeDefinition(
        name="Carbon Neutral Certificate Recipe",
        result_item="Carbon Neutral Certificate",
        result_quantity=1,
        ingredients=[
            ("Green Energy Certificate", 3),
            ("Carbon Credit", 5)
        ],
        description="Official certification for 100% carbon-negative operations.",
        item_type="special",
        rarity=5,
        base_value=150.00
    ),
    "eco_drone_blueprint": RecipeDefinition(
        name="Eco Drone Blueprint",
        result_item="Eco Drone",
        result_quantity=1,
        ingredients=[
            ("Composite Alloy", 15),
            ("Nano Coating", 5),
            ("Solar Panel", 5),
            ("Eco Badge", 3)
        ],
        description="AI-powered drone for precision farming and eco-monitoring.",
        item_type="blueprint",
        rarity=5,
        base_value=95.00
    ),
    "rainwater_system_blueprint": RecipeDefinition(
        name="Rainwater Harvesting Blueprint",
        result_item="Rainwater Harvesting System",
        result_quantity=1,
        ingredients=[
            ("Recycled Plastic", 50),
            ("Glass", 20),
            ("Titanium", 10)
        ],
        description="Advanced water conservation system with filtration.",
        item_type="blueprint",
        rarity=4,
        base_value=45.00
    ),
    "hybrid_seeds": RecipeDefinition(
        name="Hybrid Crop Seeds",
        result_item="Hybrid Crop Seeds",
        result_quantity=5,
        ingredients=[
            ("Sustainable Seed", 3),
            ("Organic Compost", 10),
            ("Eco Fertilizer", 2)
        ],
        description="High-yield drought-resistant seeds for sustainable farming.",
        item_type="consumable",
        rarity=3,
        base_value=12.00
    ),
    "smart_grid_blueprint": RecipeDefinition(
        name="Smart Grid Controller Blueprint",
        result_item="Smart Grid Controller",
        result_quantity=1,
        ingredients=[
            ("Sustainable Energy System", 1),
            ("Eco Badge", 5),
            ("Carbon Fiber", 10)
        ],
        description="Intelligent energy management system for zero-waste power distribution.",
        item_type="blueprint",
        rarity=5,
        base_value=110.00
    ),
    "biofuel_blueprint": RecipeDefinition(
        name="Biofuel Generator Blueprint",
        result_item="Biofuel Generator",
        result_quantity=1,
        ingredients=[
            ("Organic Compost", 20),
            ("Recycled Plastic", 30),
            ("Carbon Fiber", 15)
        ],
        description="Converts organic waste into clean energy for farm machinery.",
        item_type="blueprint",
        rarity=4,
        base_value=55.00
    ),
    "eco_packaging": RecipeDefinition(
        name="Eco-Friendly Packaging",
        result_item="Eco-Friendly Packaging",
        result_quantity=10,
        ingredients=[
            ("Recycled Plastic", 20),
            ("Organic Fiber", 5)
        ],
        description="Sustainable packaging solution for farm products.",
        item_type="consumable",
        rarity=3,
        base_value=8.00
    ),
    "nanobot_fertilizer": RecipeDefinition(
        name="Nanobot Fertilizer Recipe",
        result_item="Nanobot Fertilizer",
        result_quantity=1,
        ingredients=[
            ("Nano Coating", 2),
            ("Eco Fertilizer", 5),
            ("Gaia's Embrace", 1)
        ],
        description="Next-generation fertilizer with smart nutrient delivery system.",
        item_type="consumable",
        rarity=5,
        base_value=200.00
    ),
    "pest_control": RecipeDefinition(
        name="Organic Pest Control Recipe",
        result_item="Organic Pest Control",
        result_quantity=5,
        ingredients=[
            ("Organic Compost", 10),
            ("Sustainable Seed", 5),
            ("Eco Badge", 2)
        ],
        description="Natural pest deterrent made from fermented plant compounds.",
        item_type="consumable",
        rarity=3,
        base_value=18.00
    ),
    "eco_storage_blueprint": RecipeDefinition(
        name="Eco Storage Blueprint",
        result_item="Eco Storage Unit",
        result_quantity=1,
        ingredients=[
            ("Recycled Plastic", 40),
            ("Composite Alloy", 10),
            ("Solar Panel", 3)
        ],
        description="Climate-controlled storage powered by renewable energy.",
        item_type="blueprint",
        rarity=4,
        base_value=65.00
    ),
    "solar_irrigation_blueprint": RecipeDefinition(
        name="Solar Irrigation Blueprint",
        result_item="Solar-Powered Irrigation System",
        result_quantity=1,
        ingredients=[
            ("Eco Irrigation System", 1),
            ("Premium Solar Panel", 3)
        ],
        description="Fully solar-powered smart irrigation network.",
        item_type="blueprint",
        rarity=4,
        base_value=60.00
    ),
    "eco_home_bundle": RecipeDefinition(
        name="Eco Home Bundle Blueprint",
        result_item="Eco Home Bundle",
        result_quantity=1,
        ingredients=[
            ("Advanced Greenhouse", 1),
            ("Sustainable Energy System", 1),
            ("Eco Irrigation System", 1)
        ],
        description="Complete sustainable living package for modern farmers.",
        item_type="blueprint",
        rarity=5,
        base_value=250.00
    )
}