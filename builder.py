from gdpc import Block
from gdpc.geometry import placeCuboid

from houses_data import generate_houses


def get_height(world_slice, x, z):

    return world_slice.heightmaps[
        "MOTION_BLOCKING_NO_LEAVES"
    ][x, z]


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

    from houses import build_house

    amount = village.get("population", 5)

    houses = generate_houses(village, amount)

    for house in houses:

        try:
            build_house(editor, world_slice, house)

        except Exception as e:
            print(f"Erreur lors de la construction d'une maison : {e}")

    village["houses"] = houses