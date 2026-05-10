import config

from random import randint
from random import choice

from gdpc import Block
from gdpc.geometry import placeCuboid
from gdpc.geometry import placeCuboidHollow

from builder import get_height


def create_house(x, z, biome, resource):

    return {
        "x": x,
        "z": z,
        "biome": biome,
        "resource": resource,
        "owner": None
    }


def generate_houses(village, amount):

    houses = []

    for _ in range(amount):

        hx = max(
            config.MAP_MARGIN,
            min(
                village["x"] + randint(-15, 15),
                config.WORLD_SIZE - config.MAP_MARGIN
            )
        )

        hz = max(
            config.MAP_MARGIN,
            min(
                village["z"] + randint(-15, 15),
                config.WORLD_SIZE - config.MAP_MARGIN
            )
        )

        house = create_house(
            hx,
            hz,
            village["biome"],
            village["resource"]
        )

        houses.append(house)

    return houses


def get_wall_material(resource):

    if resource == "wood":

        return choice([
            Block("oak_planks"),
            Block("spruce_planks")
        ])

    elif resource == "stone":

        return choice([
            Block("stone_bricks"),
            Block("cobblestone")
        ])

    elif resource == "sand":

        return Block("sandstone")

    return Block("oak_planks")


def build_house(editor, world_slice, house):

    x = house["x"]
    z = house["z"]

    y = get_height(world_slice, x, z) - 1

    wall_block = get_wall_material(
        house["resource"]
    )

    width = 5
    depth = 6
    height = 5

    # structure extérieure
    placeCuboidHollow(
        editor,
        (x, y, z),
        (x + width, y + height, z + depth),
        wall_block
    )

    # intérieur vide
    placeCuboid(
        editor,
        (x + 1, y + 1, z + 1),
        (x + width - 1, y + height - 1, z + depth - 1),
        Block("air")
    )

    # porte
    editor.placeBlock(
        (x + 2, y + 1, z),
        Block("oak_door")
    )

    # toit gauche
    for dz in range(-1, depth + 2):

        editor.placeBlock(
            (x - 1, y + height + 1, z + dz),
            Block(
                "oak_stairs",
                {
                    "facing": "east"
                }
            )
        )

    # toit droite
    for dz in range(-1, depth + 2):

        editor.placeBlock(
            (x + width + 1, y + height + 1, z + dz),
            Block(
                "oak_stairs",
                {
                    "facing": "west"
                }
            )
        )

    # centre du toit
    placeCuboid(
        editor,
        (x, y + height + 1, z - 1),
        (x + width, y + height + 1, z + depth + 1),
        Block("oak_planks")
    )