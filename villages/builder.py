from gdpc import Block
from gdpc.geometry import placeCuboid

from villages.houses.houses_data import generate_houses


def get_height(world_slice, x, z):

    heightmap = world_slice.heightmaps[
        "MOTION_BLOCKING_NO_LEAVES"
    ]

    max_x = heightmap.shape[0] - 1
    max_z = heightmap.shape[1] - 1

    safe_x = max(0, min(x, max_x))
    safe_z = max(0, min(z, max_z))

    return heightmap[safe_x, safe_z]


def clear_area(
    editor,
    x1,
    y1,
    z1,
    x2,
    y2,
    z2
):

    placeCuboid(
        editor,
        (x1, y1, z1),
        (x2, y2, z2),
        Block("air")
    )


def build_village(editor, world_slice, village):

    from villages.houses.houses import build_house

    amount = village.get("population", 5)

    houses = generate_houses(village, amount)

    for house in houses:

        try:
            build_house(editor, world_slice, house)

        except Exception as e:
            print(f"Erreur lors de la construction d'une maison : {e}")

    village["houses"] = houses