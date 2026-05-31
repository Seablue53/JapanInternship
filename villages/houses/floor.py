from gdpc import Block
from gdpc.geometry import placeCuboid


def place_floor(editor, x, y, z, width, depth, floor_inside_block):
    """
    Pose le sol intérieur de la maison.
    Couvre toute la surface intérieure (sans les murs).
    """

    placeCuboid(
        editor,
        (x + 1,         y, z + 1),
        (x + width - 1, y, z + depth - 1),
        floor_inside_block
    )