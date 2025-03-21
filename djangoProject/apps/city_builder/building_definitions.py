from decimal import Decimal

class BuildingDefinition:
    """
    A detailed container for building blueprint data with multi-level upgrades.
    """
    def __init__(self, name, description, base_cost, resource_requirements,
                 sustainability_bonus, upgrade_multiplier, upgrades=None, upgrade_materials=None, produces_resource=None,
                 production_rate=Decimal("0.00")):
        self.name = name
        self.description = description
        self.base_cost = Decimal(base_cost)
        self.resource_requirements = resource_requirements  # Base cost materials for initial construction
        self.sustainability_bonus = Decimal(sustainability_bonus)
        self.upgrade_multiplier = Decimal(upgrade_multiplier)
        self.upgrades = upgrades or {}         # Additional currency cost and bonus increase per level
        self.upgrade_materials = upgrade_materials or {}  # Additional material requirements per upgrade level

        self.produces_resource = produces_resource  # e.g. "wood", "energy", etc.
        self.production_rate = Decimal(production_rate)  # units produced per hour


BUILDING_DEFINITIONS = {
    "solar_panel": BuildingDefinition(
        name="Solar Panel",
        description="Generates renewable energy to lower your city's carbon footprint.",
        base_cost="100.00",
        resource_requirements={
            "glass": 20,
            "metal": 10,
            "basic electronics": 5,
        },
        sustainability_bonus="5.00",
        upgrade_multiplier="1.5",
        upgrades={
            2: {"additional_cost": Decimal("50.00"), "bonus_increase": Decimal("2.50")},
            3: {"additional_cost": Decimal("75.00"), "bonus_increase": Decimal("2.50")},
            4: {"additional_cost": Decimal("112.50"), "bonus_increase": Decimal("2.50")},
            5: {"additional_cost": Decimal("168.75"), "bonus_increase": Decimal("2.50")},
        },
        upgrade_materials={
            2: {"glass": 10, "metal": 5, "basic electronics": 3},
            3: {"glass": 15, "metal": 8, "basic electronics": 5},
            4: {"reinforced glass": 20, "metal": 11, "basic electronics": 7},
            5: {"reinforced glass": 25, "metal": 14, "basic electronics": 9},
        }
    ),
    "greenhouse": BuildingDefinition(
        name="Greenhouse",
        description="Provides controlled growing conditions to boost crop yield.",
        base_cost="200.00",
        resource_requirements={
            "glass": 40,
            "eco-concrete": 20,
            "wood": 30,
        },
        sustainability_bonus="10.00",
        upgrade_multiplier="1.3",
        upgrades={
            2: {"additional_cost": Decimal("100.00"), "bonus_increase": Decimal("5.00")},
            3: {"additional_cost": Decimal("150.00"), "bonus_increase": Decimal("5.00")},
            4: {"additional_cost": Decimal("195.00"), "bonus_increase": Decimal("5.00")},
            5: {"additional_cost": Decimal("253.50"), "bonus_increase": Decimal("5.00")},
        },
        upgrade_materials={
            2: {"glass": 20, "eco-concrete": 10, "wood": 10},
            3: {"glass": 30, "eco-concrete": 15, "wood": 15},
            4: {"reinforced glass": 40, "eco-concrete": 20, "wood": 20},
            5: {"reinforced glass": 50, "eco-concrete": 25, "wood": 25},
        }
    ),
    "ev_charging": BuildingDefinition(
        name="EV Charging Hub",
        description="A network of fast-charging stations for electric vehicles.",
        base_cost="180.00",
        resource_requirements={
            "metal": 50,
            "basic electronics": 70,
            "plastic": 30,
        },
        sustainability_bonus="8.00",
        upgrade_multiplier="1.6",
        upgrades={
            2: {"additional_cost": Decimal("108.00"), "bonus_increase": Decimal("2.00")},
            3: {"additional_cost": Decimal("172.80"), "bonus_increase": Decimal("2.00")},
            4: {"additional_cost": Decimal("276.48"), "bonus_increase": Decimal("2.00")},
            5: {"additional_cost": Decimal("442.37"), "bonus_increase": Decimal("2.00")},
        },
        upgrade_materials={
            2: {"metal": 25, "basic electronics": 35, "plastic": 15},
            3: {"metal": 40, "basic electronics": 56, "plastic": 24},
            4: {"metal": 64, "basic electronics": 80, "plastic": 38},
            5: {"metal": 102, "basic electronics": 110, "plastic": 61},
        }
    ),
    "smart_grid": BuildingDefinition(
        name="Smart Grid Station",
        description="An advanced energy distribution network with AI optimization.",
        base_cost="400.00",
        resource_requirements={
            "advanced electronics": 120,
            "metal": 80,
            "plastic": 50,
        },
        sustainability_bonus="15.00",
        upgrade_multiplier="1.7",
        upgrades={
            2: {"additional_cost": Decimal("280.00"), "bonus_increase": Decimal("3.50")},
            3: {"additional_cost": Decimal("476.00"), "bonus_increase": Decimal("3.50")},
            4: {"additional_cost": Decimal("809.20"), "bonus_increase": Decimal("3.50")},
            5: {"additional_cost": Decimal("1375.64"), "bonus_increase": Decimal("3.50")},
        },
        upgrade_materials={
            2: {"advanced electronics": 60, "metal": 40, "plastic": 25},
            3: {"advanced electronics": 102, "metal": 68, "plastic": 43},
            4: {"advanced electronics": 173, "metal": 116, "plastic": 73},
            5: {"advanced electronics": 294, "metal": 197, "plastic": 124},
        }
    ),
    "industrial": BuildingDefinition(
        name="Industrial Complex",
        description="A multipurpose facility for manufacturing sustainable components.",
        base_cost="500.00",
        resource_requirements={
            "metal": 150,
            "advanced electronics": 50,
            "eco-concrete": 100,
        },
        sustainability_bonus="18.00",
        upgrade_multiplier="1.6",
        upgrades={
            2: {"additional_cost": Decimal("300.00"), "bonus_increase": Decimal("4.00")},
            3: {"additional_cost": Decimal("480.00"), "bonus_increase": Decimal("4.00")},
            4: {"additional_cost": Decimal("768.00"), "bonus_increase": Decimal("4.00")},
            5: {"additional_cost": Decimal("1228.80"), "bonus_increase": Decimal("4.00")},
        },
        upgrade_materials={
            2: {"metal": 75, "advanced electronics": 25, "eco-concrete": 50},
            3: {"metal": 110, "advanced electronics": 40, "eco-concrete": 70},
            4: {"metal": 165, "advanced electronics": 55, "eco-concrete": 105},
            5: {"metal": 250, "advanced electronics": 80, "eco-concrete": 150},
        },
        produces_resource="metal",
        production_rate=Decimal("0.50"),
    ),
    "algae_reactor": BuildingDefinition(
        name="Algae Biofuel Reactor",
        description="Converts algae into clean biofuels using photosynthesis.",
        base_cost="220.00",
        resource_requirements={
            "glass": 80,
            "plastic": 60,
            "biomass": 40,
        },
        sustainability_bonus="9.00",
        upgrade_multiplier="1.5",
        upgrades={
            2: {"additional_cost": Decimal("110.00"), "bonus_increase": Decimal("2.25")},
            3: {"additional_cost": Decimal("165.00"), "bonus_increase": Decimal("2.25")},
            4: {"additional_cost": Decimal("247.50"), "bonus_increase": Decimal("2.25")},
            5: {"additional_cost": Decimal("371.25"), "bonus_increase": Decimal("2.25")},
        },
        upgrade_materials={
            2: {"glass": 40, "plastic": 30, "biomass": 20},
            3: {"glass": 60, "plastic": 45, "biomass": 30},
            4: {"reinforced glass": 90, "plastic": 68, "biomass": 45},
            5: {"reinforced glass": 135, "plastic": 101, "biomass": 68},
        }
    ),
    "urban_forest": BuildingDefinition(
        name="Urban Forest",
        description="High-density tree planting for carbon sequestration.",
        base_cost="150.00",
        resource_requirements={
            "wood": 100,
            "fertilizer": 50,
            "tools": 30,
        },
        sustainability_bonus="18.00",
        upgrade_multiplier="1.4",
        upgrades={
            2: {"additional_cost": Decimal("60.00"), "bonus_increase": Decimal("4.00")},
            3: {"additional_cost": Decimal("84.00"), "bonus_increase": Decimal("4.00")},
            4: {"additional_cost": Decimal("117.60"), "bonus_increase": Decimal("4.00")},
            5: {"additional_cost": Decimal("164.64"), "bonus_increase": Decimal("4.00")},
        },
        upgrade_materials={
            2: {"wood": 50, "fertilizer": 25, "tools": 15},
            3: {"wood": 70, "fertilizer": 35, "tools": 21},
            4: {"wood": 98, "fertilizer": 49, "tools": 29},
            5: {"wood": 137, "fertilizer": 69, "tools": 41},
        }
    ),
    "tidal_generator": BuildingDefinition(
        name="Tidal Generator",
        description="Converts ocean tidal movements into electricity.",
        base_cost="650.00",
        resource_requirements={
            "metal": 200,
            "concrete": 150,
            "waterproofing": 80,
        },
        sustainability_bonus="22.00",
        upgrade_multiplier="1.6",
        upgrades={
            2: {"additional_cost": Decimal("390.00"), "bonus_increase": Decimal("5.50")},
            3: {"additional_cost": Decimal("624.00"), "bonus_increase": Decimal("5.50")},
            4: {"additional_cost": Decimal("998.40"), "bonus_increase": Decimal("5.50")},
            5: {"additional_cost": Decimal("1597.44"), "bonus_increase": Decimal("5.50")},
        },
        upgrade_materials={
            2: {"metal": 100, "concrete": 75, "waterproofing": 40},
            3: {"metal": 160, "concrete": 120, "waterproofing": 64},
            4: {"metal": 256, "concrete": 192, "waterproofing": 102},
            5: {"metal": 410, "concrete": 307, "waterproofing": 163},
        }
    ),
    "green_roof": BuildingDefinition(
        name="Green Roof Complex",
        description="Vegetated roof installations for insulation and biodiversity.",
        base_cost="120.00",
        resource_requirements={
            "plants": 80,
            "soil": 120,
            "drainage": 40,
        },
        sustainability_bonus="7.00",
        upgrade_multiplier="1.3",
        upgrades={
            2: {"additional_cost": Decimal("36.00"), "bonus_increase": Decimal("1.75")},
            3: {"additional_cost": Decimal("46.80"), "bonus_increase": Decimal("1.75")},
            4: {"additional_cost": Decimal("60.84"), "bonus_increase": Decimal("1.75")},
            5: {"additional_cost": Decimal("79.09"), "bonus_increase": Decimal("1.75")},
        },
        upgrade_materials={
            2: {"plants": 40, "soil": 60, "drainage": 20},
            3: {"plants": 52, "soil": 78, "drainage": 26},
            4: {"plants": 68, "soil": 101, "drainage": 34},
            5: {"plants": 88, "soil": 132, "drainage": 44},
        }
    ),
    "bamboo_plantation": BuildingDefinition(
        name="Bamboo Plantation",
        description="Fast-growing bamboo for sustainable construction materials.",
        base_cost="90.00",
        resource_requirements={
            "fertilizer": 40,
            "tools": 20,
        },
        sustainability_bonus="6.00",
        upgrade_multiplier="1.5",
        upgrades={
            2: {"additional_cost": Decimal("45.00"), "bonus_increase": Decimal("1.50")},
            3: {"additional_cost": Decimal("67.50"), "bonus_increase": Decimal("1.50")},
            4: {"additional_cost": Decimal("101.25"), "bonus_increase": Decimal("1.50")},
            5: {"additional_cost": Decimal("151.88"), "bonus_increase": Decimal("1.50")},
        },
        upgrade_materials={
            2: {"fertilizer": 20, "tools": 10},
            3: {"fertilizer": 30, "tools": 15},
            4: {"fertilizer": 45, "tools": 23},
            5: {"fertilizer": 68, "tools": 34},
        }
    ),

    # New Building Definitions:

    "wind_turbine": BuildingDefinition(
        name="Wind Turbine",
        description="Generates clean energy by harnessing wind power.",
        base_cost="120.00",
        resource_requirements={
            "reinforced glass": 10,
            "metal": 30,
            "basic electronics": 10,
        },
        sustainability_bonus="7.00",
        upgrade_multiplier="1.4",
        upgrades={
            2: {"additional_cost": Decimal("40.00"), "bonus_increase": Decimal("2.00")},
            3: {"additional_cost": Decimal("56.00"), "bonus_increase": Decimal("2.00")},
            4: {"additional_cost": Decimal("78.40"), "bonus_increase": Decimal("2.00")},
            5: {"additional_cost": Decimal("109.76"), "bonus_increase": Decimal("2.00")},
        },
        upgrade_materials={
            2: {"reinforced glass": 5, "metal": 15, "basic electronics": 5},
            3: {"reinforced glass": 7, "metal": 21, "basic electronics": 7},
            4: {"reinforced glass": 10, "metal": 30, "basic electronics": 10},
            5: {"reinforced glass": 12, "metal": 40, "basic electronics": 12},
        }
    ),
    "hydroelectric_dam": BuildingDefinition(
        name="Hydroelectric Dam",
        description="Harnesses water flow to produce renewable energy.",
        base_cost="500.00",
        resource_requirements={
            "eco-concrete": 150,
            "metal": 100,
            "basic electronics": 30,
        },
        sustainability_bonus="18.00",
        upgrade_multiplier="1.5",
        upgrades={
            2: {"additional_cost": Decimal("200.00"), "bonus_increase": Decimal("4.00")},
            3: {"additional_cost": Decimal("300.00"), "bonus_increase": Decimal("4.00")},
            4: {"additional_cost": Decimal("450.00"), "bonus_increase": Decimal("4.00")},
            5: {"additional_cost": Decimal("675.00"), "bonus_increase": Decimal("4.00")},
        },
        upgrade_materials={
            2: {"eco-concrete": 75, "metal": 50, "basic electronics": 15},
            3: {"eco-concrete": 100, "metal": 70, "basic electronics": 20},
            4: {"eco-concrete": 150, "metal": 100, "basic electronics": 30},
            5: {"eco-concrete": 200, "metal": 140, "basic electronics": 40},
        }
    ),
    "geothermal_plant": BuildingDefinition(
        name="Geothermal Plant",
        description="Harnesses Earth's natural heat for clean power.",
        base_cost="600.00",
        resource_requirements={
            "eco-concrete": 200,
            "metal": 150,
            "advanced electronics": 50,
        },
        sustainability_bonus="20.00",
        upgrade_multiplier="1.6",
        upgrades={
            2: {"additional_cost": Decimal("250.00"), "bonus_increase": Decimal("3.50")},
            3: {"additional_cost": Decimal("400.00"), "bonus_increase": Decimal("3.50")},
            4: {"additional_cost": Decimal("640.00"), "bonus_increase": Decimal("3.50")},
            5: {"additional_cost": Decimal("1024.00"), "bonus_increase": Decimal("3.50")},
        },
        upgrade_materials={
            2: {"eco-concrete": 100, "metal": 75, "advanced electronics": 25},
            3: {"eco-concrete": 150, "metal": 100, "advanced electronics": 35},
            4: {"eco-concrete": 200, "metal": 150, "advanced electronics": 50},
            5: {"eco-concrete": 300, "metal": 200, "advanced electronics": 75},
        }
    ),
    "eco_recycling_center": BuildingDefinition(
        name="Eco Recycling Center",
        description="Processes waste into reusable materials to conserve resources.",
        base_cost="250.00",
        resource_requirements={
            "metal": 60,
            "eco-concrete": 80,
            "advanced electronics": 30,
        },
        sustainability_bonus="12.00",
        upgrade_multiplier="1.5",
        upgrades={
            2: {"additional_cost": Decimal("120.00"), "bonus_increase": Decimal("2.50")},
            3: {"additional_cost": Decimal("180.00"), "bonus_increase": Decimal("2.50")},
            4: {"additional_cost": Decimal("270.00"), "bonus_increase": Decimal("2.50")},
            5: {"additional_cost": Decimal("405.00"), "bonus_increase": Decimal("2.50")},
        },
        upgrade_materials={
            2: {"metal": 30, "eco-concrete": 40, "advanced electronics": 15},
            3: {"metal": 45, "eco-concrete": 60, "advanced electronics": 20},
            4: {"metal": 60, "eco-concrete": 80, "advanced electronics": 25},
            5: {"metal": 75, "eco-concrete": 100, "advanced electronics": 30},
        }
    ),
    "urban_farm": BuildingDefinition(
        name="Urban Farm",
        description="Enables urban food production using sustainable methods.",
        base_cost="150.00",
        resource_requirements={
            "wood": 50,
            "eco-concrete": 30,
            "organic compost": 20,
        },
        sustainability_bonus="8.00",
        upgrade_multiplier="1.3",
        upgrades={
            2: {"additional_cost": Decimal("60.00"), "bonus_increase": Decimal("2.00")},
            3: {"additional_cost": Decimal("80.00"), "bonus_increase": Decimal("2.00")},
            4: {"additional_cost": Decimal("100.00"), "bonus_increase": Decimal("2.00")},
            5: {"additional_cost": Decimal("120.00"), "bonus_increase": Decimal("2.00")},
        },
        upgrade_materials={
            2: {"wood": 25, "eco-concrete": 15, "organic compost": 10},
            3: {"wood": 35, "eco-concrete": 20, "organic compost": 15},
            4: {"wood": 50, "eco-concrete": 30, "organic compost": 20},
            5: {"wood": 70, "eco-concrete": 40, "organic compost": 25},
        }
    ),
    "biomass_plant": BuildingDefinition(
        name="Biomass Plant",
        description="Converts organic waste into energy and fertilizer.",
        base_cost="300.00",
        resource_requirements={
            "organic compost": 40,
            "wood": 30,
            "metal": 20,
        },
        sustainability_bonus="10.00",
        upgrade_multiplier="1.4",
        upgrades={
            2: {"additional_cost": Decimal("120.00"), "bonus_increase": Decimal("3.00")},
            3: {"additional_cost": Decimal("168.00"), "bonus_increase": Decimal("3.00")},
            4: {"additional_cost": Decimal("235.20"), "bonus_increase": Decimal("3.00")},
            5: {"additional_cost": Decimal("329.28"), "bonus_increase": Decimal("3.00")},
        },
        upgrade_materials={
            2: {"organic compost": 20, "wood": 15, "metal": 10},
            3: {"organic compost": 30, "wood": 20, "metal": 15},
            4: {"organic compost": 40, "wood": 30, "metal": 20},
            5: {"organic compost": 50, "wood": 40, "metal": 25},
        }
    ),
}