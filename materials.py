from random import choice


MATERIALS = {
    "wood": {
        "wall":   ["spruce_planks", "oak_planks", "birch_planks"],
        "log":    ["spruce_log", "oak_log", "birch_log"],
        "slab":   ["spruce_slab", "oak_slab"],
        "stairs": ["spruce_stairs", "oak_stairs"],
        "glass":  "glass_pane",
        "floor":  "dirt_path",
        "door":   "spruce_door",
        "light":  "lantern",
        "fence":  "spruce_fence",
    },
    "stone": {
        "wall":   ["stone_bricks", "cobblestone", "andesite"],
        "log":    ["stone_bricks", "andesite"],
        "slab":   ["stone_brick_slab", "cobblestone_slab"],
        "stairs": ["stone_brick_stairs", "cobblestone_stairs"],
        "glass":  "glass_pane",
        "floor":  "stone_bricks",
        "door":   "iron_door",
        "light":  "sea_lantern",
        "fence":  "iron_bars",
    },
    "sand": {
        "wall":   ["sandstone", "smooth_sandstone", "cut_sandstone"],
        "log":    ["smooth_sandstone", "cut_sandstone"],
        "slab":   ["sandstone_slab", "smooth_sandstone_slab"],
        "stairs": ["sandstone_stairs", "smooth_sandstone_stairs"],
        "glass":  "glass_pane",
        "floor":  "sand",
        "door":   "acacia_door",
        "light":  "torch",
        "fence":  "acacia_fence",
    },
    "food": {
        "wall":   ["oak_planks", "mud_bricks"],
        "log":    ["oak_log", "stripped_oak_log"],
        "slab":   ["oak_slab", "mud_brick_slab"],
        "stairs": ["oak_stairs", "mud_brick_stairs"],
        "glass":  "glass_pane",
        "floor":  "grass_block",
        "door":   "oak_door",
        "light":  "torch",
        "fence":  "oak_fence",
    },
}

DEFAULT_MATERIALS = MATERIALS["wood"]


def get_materials(resource):
    return MATERIALS.get(resource, DEFAULT_MATERIALS)


def pick(lst):
    """Choisit un élément aléatoire dans une liste."""
    return choice(lst)