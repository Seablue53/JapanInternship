

BIOME_RESOURCES = {
    "forest": "wood",
    "plains": "food",
    "desert": "sand",
    "mountain": "stone",
    "jungle": "wood"
}


def detect_resource(biome):

    for key in BIOME_RESOURCES:

        if key in biome:
            return BIOME_RESOURCES[key]

    return "basic"


def build_grid(editor, world_size, grid_size):

    zones = []

    for x in range(0, world_size, grid_size):

        for z in range(0, world_size, grid_size):

            biome = editor.getBiome((x, 0, z))

            zones.append({
                "x": x,
                "z": z,
                "biome": biome,
                "resource": detect_resource(biome)
            })

    return zones