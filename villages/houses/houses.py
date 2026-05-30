from random import randint, choice

from gdpc import Block
from gdpc.geometry import placeCuboid, placeCuboidHollow

from villages.builder import get_height

from villages.houses.houses_data import create_house, generate_houses
from villages.materials import get_materials, pick
from villages.houses.roof import build_roof
from villages.houses.door import place_door


def _ground_level(world_slice, x, z, width, depth):
    """
    Retourne le Y max sous toute la surface de la maison.
    Garantit que la fondation est toujours au-dessus du terrain.
    """

    y_max = 0

    for dx in range(width + 1):
        for dz in range(depth + 1):
            y = get_height(world_slice, x + dx, z + dz)
            if y > y_max:
                y_max = y

    return y_max


def _fill_foundation(editor, world_slice, x, z, width, depth, y_base, fill_block):
    """
    Pour chaque colonne sous la maison, remplit depuis le sol réel
    jusqu'à y_base pour combler les creux du terrain.
    """

    for dx in range(width + 1):
        for dz in range(depth + 1):
            y_col = get_height(world_slice, x + dx, z + dz) - 1

            if y_col < y_base:
                placeCuboid(
                    editor,
                    (x + dx, y_col + 1, z + dz),
                    (x + dx, y_base,    z + dz),
                    fill_block
                )


def build_house(editor, world_slice, house):

    x = house["x"]
    z = house["z"]

    mat = get_materials(house["resource"])

    wall_name  = pick(mat["wall"])
    log_name   = pick(mat["log"])
    slab_name  = pick(mat["slab"])
    stair_name = pick(mat["stairs"])
    glass_name = mat["glass"]
    floor_name = mat["floor"]
    door_name  = mat["door"]
    light_name = mat["light"]

    wall_block  = Block(wall_name)
    log_block   = Block(log_name)
    glass_block = Block(glass_name)
    floor_block = Block(floor_name)
    air_block   = Block("air")

    width  = randint(5, 8)
    depth  = randint(5, 8)
    height = randint(4, 5)

    orientation = choice(["north", "south", "east", "west"])


    y = _ground_level(world_slice, x, z, width, depth) - 1

    _fill_foundation(
        editor, world_slice,
        x, z, width, depth,
        y, wall_block
    )


    placeCuboid(
        editor,
        (x,         y,     z),
        (x + width, y,     z + depth),
        floor_block
    )


    placeCuboidHollow(
        editor,
        (x,         y + 1,      z),
        (x + width, y + height, z + depth),
        wall_block
    )


    placeCuboid(
        editor,
        (x + 1,         y + 1,          z + 1),
        (x + width - 1, y + height - 1, z + depth - 1),
        air_block
    )


    for cx, cz in [
        (x,          z),
        (x + width,  z),
        (x,          z + depth),
        (x + width,  z + depth),
    ]:
        for dy in range(1, height):
            editor.placeBlock((cx, y + dy, cz), log_block)


    win_y = y + 2
    mid_x = x + width // 2
    mid_z = z + depth // 2

    for win_x in [mid_x - 1, mid_x + 1]:
        if x < win_x < x + width:
            editor.placeBlock((win_x, win_y, z),         glass_block)
            editor.placeBlock((win_x, win_y, z + depth), glass_block)

    for win_z in [mid_z - 1, mid_z + 1]:
        if z < win_z < z + depth:
            editor.placeBlock((x,         win_y, win_z), glass_block)
            editor.placeBlock((x + width, win_y, win_z), glass_block)


    build_roof(
        editor,
        x, y + height, z,
        width, depth,
        orientation,
        stair_name, slab_name,
        log_name
    )


    place_door(
        editor,
        x, y, z,
        width, depth,
        orientation,
        door_name
    )

    editor.placeBlock(
        (x + width // 2, y + height - 1, z + depth // 2),
        Block(light_name)
    )