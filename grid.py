

BIOME_RESOURCES = {

    # Wood
    "forest": "wood",
    "birch": "wood",
    "dark_forest": "wood",
    "taiga": "wood",
    "old_growth": "wood",
    "jungle": "wood",
    "bamboo": "wood",
    "mangrove": "wood",
    "grove": "wood",
    "swamp": "wood",

    # Food
    "plains": "food",
    "savanna": "food",
    "river": "food",
    "ocean": "food",
    "beach": "food",
    "snowy_plains": "food",
    "meadow": "food",

    # Sand
    "desert": "sand",

    # Stone
    "mountain": "stone",
    "windswept": "stone",
    "stony": "stone",
    "peaks": "stone",
    "badlands": "stone",
    "lush_caves": "stone"
}

def detect_resource(biome):

    for key in BIOME_RESOURCES:

        biome = biome.lower()
        if key in biome:
            return BIOME_RESOURCES[key]

    return "food"


def build_grid(editor, world_size, grid_size):

    zones = []

    for x in range(0, world_size, grid_size):

        for z in range(0, world_size, grid_size):

            biome = editor.getBiome((x, 256, z))

            zones.append({
                "x": x,
                "z": z,
                "biome": biome,
                "resource": detect_resource(biome)
            })

    return zones