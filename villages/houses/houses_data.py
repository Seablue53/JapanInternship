import config
import math

from random import randint


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