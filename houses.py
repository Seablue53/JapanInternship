from random import randint, choice

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

        hx = village["x"] + randint(-15, 15)
        hz = village["z"] + randint(-15, 15)

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

    placeCuboidHollow(
        editor,
        (x, y, z),
        (x + width, y + height, z + depth),
        wall_block
    )

    placeCuboid(
        editor,
        (x + 1, y + 1, z + 1),
        (x + width - 1, y + height - 1, z + depth - 1),
        Block("air")
    )

    editor.placeBlock(
        (x + 2, y + 1, z),
        Block("oak_door")
    )