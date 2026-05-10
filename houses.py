import config

from random import randint
from random import choice

from gdpc import Block
from gdpc.geometry import placeCuboid
from gdpc.geometry import placeCuboidHollow

from builder import get_height

import math


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

    center_x = village["x"]
    center_z = village["z"]

    min_radius = 15
    max_radius = 45

    attempts = 0

    while len(houses) < amount and attempts < 500:

        attempts += 1

        angle = randint(0, 360)

        radius = randint(
            min_radius,
            max_radius
        )

        hx = int(
            center_x +
            math.cos(math.radians(angle)) * radius
        )

        hz = int(
            center_z +
            math.sin(math.radians(angle)) * radius
        )

        hx = max(
            config.MAP_MARGIN,
            min(
                hx,
                config.WORLD_SIZE - config.MAP_MARGIN
            )
        )

        hz = max(
            config.MAP_MARGIN,
            min(
                hz,
                config.WORLD_SIZE - config.MAP_MARGIN
            )
        )

        # évite les maisons trop proches
        too_close = False

        for house in houses:

            distance = (
                (hx - house["x"]) ** 2 +
                (hz - house["z"]) ** 2
            ) ** 0.5

            if distance < 14:

                too_close = True
                break

        if too_close:
            continue

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

    # tailles aléatoires
    width = randint(4, 6)
    depth = randint(4, 6)
    height = randint(3, 4)

    orientation = choice([
        "north",
        "south",
        "east",
        "west"
    ])

    # structure principale
    placeCuboidHollow(
        editor,
        (x, y, z),
        (x + width, y + height, z + depth),
        wall_block
    )

    # intérieur
    placeCuboid(
        editor,
        (x + 1, y + 1, z + 1),
        (x + width - 1, y + height - 1, z + depth - 1),
        Block("air")
    )

    roof_block = Block("oak_stairs")

    # toit orientation nord/sud
    if orientation in ["north", "south"]:

        for dz in range(depth + 1):

            editor.placeBlock(
                (x - 1, y + height + 1, z + dz),
                Block(
                    "oak_stairs",
                    {
                        "facing": "east"
                    }
                )
            )

            editor.placeBlock(
                (x + width + 1, y + height + 1, z + dz),
                Block(
                    "oak_stairs",
                    {
                        "facing": "west"
                    }
                )
            )

        placeCuboid(
            editor,
            (x, y + height + 1, z),
            (x + width, y + height + 1, z + depth),
            Block("oak_planks")
        )

    # toit orientation est/ouest
    else:

        for dx in range(width + 1):

            editor.placeBlock(
                (x + dx, y + height + 1, z - 1),
                Block(
                    "oak_stairs",
                    {
                        "facing": "south"
                    }
                )
            )

            editor.placeBlock(
                (x + dx, y + height + 1, z + depth + 1),
                Block(
                    "oak_stairs",
                    {
                        "facing": "north"
                    }
                )
            )

        placeCuboid(
            editor,
            (x, y + height + 1, z),
            (x + width, y + height + 1, z + depth),
            Block("oak_planks")
        )

    # porte selon orientation
    if orientation == "north":

        editor.placeBlock(
            (x + width // 2, y + 1, z),
            Block(
                "oak_door",
                {
                    "facing": "north"
                }
            )
        )

    elif orientation == "south":

        editor.placeBlock(
            (x + width // 2, y + 1, z + depth),
            Block(
                "oak_door",
                {
                    "facing": "south"
                }
            )
        )

    elif orientation == "east":

        editor.placeBlock(
            (x + width, y + 1, z + depth // 2),
            Block(
                "oak_door",
                {
                    "facing": "east"
                }
            )
        )

    else:

        editor.placeBlock(
            (x, y + 1, z + depth // 2),
            Block(
                "oak_door",
                {
                    "facing": "west"
                }
            )
        )