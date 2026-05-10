from random import randint, choice

from gdpc import Block
from gdpc.geometry import placeCuboid, placeCuboidHollow

from builder import get_height

from houses_data import create_house, generate_houses
from materials import get_materials, pick
from roof import build_roof
from door import place_door


def build_house(editor, world_slice, house):

    x = house["x"]
    z = house["z"]

    y = get_height(world_slice, x, z) - 1

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

    # ── Fondation ─────────────────────────────────────────────────────────────
    placeCuboid(
        editor,
        (x,         y,     z),
        (x + width, y,     z + depth),
        floor_block
    )

    # ── Murs creux ────────────────────────────────────────────────────────────
    placeCuboidHollow(
        editor,
        (x,         y + 1,      z),
        (x + width, y + height, z + depth),
        wall_block
    )

    # ── Vider l'intérieur ─────────────────────────────────────────────────────
    placeCuboid(
        editor,
        (x + 1,         y + 1,          z + 1),
        (x + width - 1, y + height - 1, z + depth - 1),
        air_block
    )

    # ── Poutres d'angle (logs verticaux) ──────────────────────────────────────
    for cx, cz in [
        (x,          z),
        (x + width,  z),
        (x,          z + depth),
        (x + width,  z + depth),
    ]:
        for dy in range(1, height + 1):
            editor.placeBlock((cx, y + dy, cz), log_block)

    # ── Fenêtres ──────────────────────────────────────────────────────────────
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

    # ── Toit ──────────────────────────────────────────────────────────────────
    build_roof(
        editor,
        x, y + height, z,
        width, depth,
        orientation,
        stair_name, slab_name,
        log_name
    )

    # ── Porte ─────────────────────────────────────────────────────────────────
    place_door(
        editor,
        x, y, z,
        width, depth,
        orientation,
        door_name
    )

    # ── Lumière intérieure ────────────────────────────────────────────────────
    editor.placeBlock(
        (x + width // 2, y + height - 1, z + depth // 2),
        Block(light_name)
    )