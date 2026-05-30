from gdpc import Block
from gdpc.geometry import placeCuboid


def _plank_from_stair(stair_name):
    return stair_name.replace("_stairs", "_planks")


def _place_roof_ns(editor, x, base_y, z, width, depth, stair_name, slab_name):
    middle = width // 2
    plank_name = _plank_from_stair(stair_name)

    for dx in range(1, middle + 1):
        yy = base_y + middle + 1 - dx

        left_x = x + middle - dx
        right_x = x + middle + dx

        left_block = Block(stair_name, {"facing": "east"})
        right_block = Block(stair_name, {"facing": "west"})

        placeCuboid(
            editor,
            (left_x, yy, z - 1),
            (left_x, yy, z + depth + 1),
            left_block
        )

        placeCuboid(
            editor,
            (right_x, yy, z - 1),
            (right_x, yy, z + depth + 1),
            right_block
        )

    top_y = base_y + middle + 1

    if width % 2 == 1:
        placeCuboid(
            editor,
            (x + middle, top_y, z - 1),
            (x + middle, top_y, z + depth + 1),
            Block(slab_name)
        )
    else:
        placeCuboid(
            editor,
            (x + middle, top_y, z - 1),
            (x + middle, top_y, z + depth + 1),
            Block(plank_name)
        )


def _place_roof_ew(editor, x, base_y, z, width, depth, stair_name, slab_name):
    middle = depth // 2
    plank_name = _plank_from_stair(stair_name)

    for dz in range(1, middle + 1):
        yy = base_y + middle + 1 - dz

        front_z = z + middle - dz
        back_z = z + middle + dz

        front_block = Block(stair_name, {"facing": "south"})
        back_block = Block(stair_name, {"facing": "north"})

        placeCuboid(
            editor,
            (x - 1, yy, front_z),
            (x + width + 1, yy, front_z),
            front_block
        )

        placeCuboid(
            editor,
            (x - 1, yy, back_z),
            (x + width + 1, yy, back_z),
            back_block
        )

    top_y = base_y + middle + 1

    if depth % 2 == 1:
        placeCuboid(
            editor,
            (x - 1, top_y, z + middle),
            (x + width + 1, top_y, z + middle),
            Block(slab_name)
        )
    else:
        placeCuboid(
            editor,
            (x - 1, top_y, z + middle),
            (x + width + 1, top_y, z + middle),
            Block(plank_name)
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
        _place_roof_ns(
            editor,
            x,
            base_y,
            z,
            width,
            depth,
            stair_name,
            slab_name
        )
    else:
        _place_roof_ew(
            editor,
            x,
            base_y,
            z,
            width,
            depth,
            stair_name,
            slab_name
        )