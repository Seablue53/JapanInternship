from gdpc import Block
from gdpc.geometry import placeCuboid


def _plank_from_stair(stair_name):
    return stair_name.replace("_stairs", "_planks")


def _place_roof_ns(editor, x, base_y, z, width, depth, stair_name, slab_name):
    """
    Pignon sur X, faîtage parallèle à Z.
    layer=0 : bords extérieurs à base_y  → triangle complet
    layer=middle : faîte
    """

    middle     = width // 2
    plank_name = _plank_from_stair(stair_name)

    for layer in range(middle + 1):
        yy      = base_y + layer
        left_x  = x + middle - layer
        right_x = x + middle + layer

        if left_x < right_x:

            placeCuboid(
                editor,
                (left_x, yy, z - 1),
                (left_x, yy, z + depth + 1),
                Block(stair_name, {"facing": "east"})
            )

            placeCuboid(
                editor,
                (right_x, yy, z - 1),
                (right_x, yy, z + depth + 1),
                Block(stair_name, {"facing": "west"})
            )

            # Remplissage entre les escaliers
            if left_x + 1 <= right_x - 1:
                placeCuboid(
                    editor,
                    (left_x + 1, yy, z - 1),
                    (right_x - 1, yy, z + depth + 1),
                    Block(plank_name)
                )

        else:
            # Faîte pair (left_x == right_x)
            placeCuboid(
                editor,
                (left_x, yy, z - 1),
                (left_x, yy, z + depth + 1),
                Block(plank_name)
            )

    # Faîte impair : slab un niveau au-dessus
    if width % 2 == 1:
        placeCuboid(
            editor,
            (x + middle, base_y + middle + 1, z - 1),
            (x + middle, base_y + middle + 1, z + depth + 1),
            Block(slab_name)
        )


def _place_roof_ew(editor, x, base_y, z, width, depth, stair_name, slab_name):
    """
    Pignon sur Z, faîtage parallèle à X.
    """

    middle     = depth // 2
    plank_name = _plank_from_stair(stair_name)

    for layer in range(middle + 1):
        yy      = base_y + layer
        front_z = z + middle - layer
        back_z  = z + middle + layer

        if front_z < back_z:

            placeCuboid(
                editor,
                (x - 1, yy, front_z),
                (x + width + 1, yy, front_z),
                Block(stair_name, {"facing": "south"})
            )

            placeCuboid(
                editor,
                (x - 1, yy, back_z),
                (x + width + 1, yy, back_z),
                Block(stair_name, {"facing": "north"})
            )

            if front_z + 1 <= back_z - 1:
                placeCuboid(
                    editor,
                    (x - 1, yy, front_z + 1),
                    (x + width + 1, yy, back_z - 1),
                    Block(plank_name)
                )

        else:
            # Faîte pair
            placeCuboid(
                editor,
                (x - 1, yy, front_z),
                (x + width + 1, yy, front_z),
                Block(plank_name)
            )

    # Faîte impair
    if depth % 2 == 1:
        placeCuboid(
            editor,
            (x - 1, base_y + middle + 1, z + middle),
            (x + width + 1, base_y + middle + 1, z + middle),
            Block(slab_name)
        )


def build_roof(
    editor,
    x,
    base_y,
    z,
    width,
    depth,
    orientation,
    stair_name,
    slab_name,
    log_name=None
):
    if orientation in ("north", "south"):
        _place_roof_ns(editor, x, base_y, z, width, depth, stair_name, slab_name)
    else:
        _place_roof_ew(editor, x, base_y, z, width, depth, stair_name, slab_name)