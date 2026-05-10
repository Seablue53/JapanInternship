from gdpc import Block
from gdpc.geometry import placeCuboid


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