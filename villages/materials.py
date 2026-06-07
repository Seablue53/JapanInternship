from random import choice


MATERIALS = {

    "wood": {
        "wall": [
            "spruce_planks",
            "oak_planks",
            "birch_planks",
            "dark_oak_planks"
        ],

        "log": [
            "spruce_log",
            "oak_log",
            "birch_log",
            "dark_oak_log"
        ],

        "slab": [
            "spruce_slab",
            "oak_slab",
            "birch_slab",
            "dark_oak_slab"
        ],

        "stairs": [
            "spruce_stairs",
            "oak_stairs",
            "birch_stairs",
            "dark_oak_stairs"
        ],

        "glass": "glass_pane",

        "floor": "dirt_path",

        "floor_inside": [
            "spruce_planks",
            "oak_planks",
            "birch_planks"
        ],

        "door": "spruce_door",

        "light": "lantern",

        "fence": "spruce_fence",
    },

    "stone": {
        "wall": [
            "stone_bricks",
            "cobblestone",
            "andesite",
            "polished_andesite"
        ],

        "log": [
            "stone_bricks",
            "andesite"
        ],

        "slab": [
            "stone_brick_slab",
            "cobblestone_slab",
            "andesite_slab"
        ],

        "stairs": [
            "stone_brick_stairs",
            "cobblestone_stairs",
            "andesite_stairs"
        ],

        "glass": "glass_pane",

        "floor": "stone_bricks",

        "floor_inside": [
            "stone_bricks",
            "polished_andesite"
        ],

        "door": "spruce_door",

        "light": "lantern",

        "fence": "cobblestone_wall",
    },

    "sand": {
        "wall": [
            "sandstone",
            "smooth_sandstone",
            "cut_sandstone",
            "red_sandstone"
        ],

        "log": [
            "smooth_sandstone",
            "cut_sandstone"
        ],

        "slab": [
            "sandstone_slab",
            "smooth_sandstone_slab",
            "red_sandstone_slab"
        ],

        "stairs": [
            "sandstone_stairs",
            "smooth_sandstone_stairs",
            "red_sandstone_stairs"
        ],

        "glass": "glass_pane",

        "floor": "sand",

        "floor_inside": [
            "smooth_sandstone",
            "cut_sandstone"
        ],

        "door": "acacia_door",

        "light": "torch",

        "fence": "acacia_fence",
    },

    "food": {
        "wall": [
            "mud_bricks",
            "packed_mud",
            "oak_planks"
        ],

        "log": [
            "oak_log",
            "stripped_oak_log"
        ],

        "slab": [
            "mud_brick_slab",
            "oak_slab"
        ],

        "stairs": [
            "mud_brick_stairs",
            "oak_stairs"
        ],

        "glass": "glass_pane",

        "floor": "grass_block",

        "floor_inside": [
            "oak_planks",
            "packed_mud"
        ],

        "door": "oak_door",

        "light": "lantern",

        "fence": "oak_fence",
    }
}

DEFAULT_MATERIALS = MATERIALS["wood"]


def get_materials(resource):
    return MATERIALS.get(resource, DEFAULT_MATERIALS)


def pick(lst):
    """Choisit un élément aléatoire dans une liste ou retourne une string."""
    if isinstance(lst, list):
        return choice(lst)
    return lst