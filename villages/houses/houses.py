from random import randint, choice

from gdpc import Block
from gdpc.geometry import placeCuboid, placeCuboidHollow

from villages.builder import get_height
from villages.houses.houses_data import create_house, generate_houses
from villages.materials import get_materials, pick
from villages.houses.roof import build_roof
from villages.houses.door import place_door
from villages.houses.floor import place_floor


TREE_BLOCKS = {
    "oak_log", "spruce_log", "birch_log", "jungle_log",
    "acacia_log", "dark_oak_log", "mangrove_log",
    "oak_leaves", "spruce_leaves", "birch_leaves", "jungle_leaves",
    "acacia_leaves", "dark_oak_leaves", "mangrove_leaves",
    "azalea_leaves", "flowering_azalea_leaves",
}

improvements = {
        "wood": [
            "crafting_table",
            "barrel",
            "fletching_table",
            "cartography_table"
        ],

        "stone": [
            "furnace",
            "blast_furnace",
            "stonecutter",
            "smithing_table"
        ],

        "sand": [
            "furnace",
            "loom",
            "cartography_table"
        ],

        "food": [
            "composter",
            "barrel",
            "crafting_table"
        ]
    }


def _ground_level(world_slice, x, z, width, depth):
    """
    Retourne le Y du centre de la maison.
    Évite de prendre le max qui crée des fondations trop hautes sur les pentes.
    """

    cx = x + width // 2
    cz = z + depth // 2

    return get_height(world_slice, cx, cz)


def _fill_foundation(editor, world_slice, x, z, width, depth, y_base, fill_block):
    """
    Comble les creux sous la fondation.
    Ne remonte que jusqu'à y_base — ne crée pas de tour sur les pentes.
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


def _clear_trees(editor, world_slice, x, z, width, depth, y_base):
    """Supprime les troncs et feuilles au-dessus de la zone de construction."""

    for dx in range(width + 1):
        for dz in range(depth + 1):
            for dy in range(20):
                cy = y_base + dy
                block = world_slice.getBlock((x + dx, cy, z + dz))

                if block is not None and block.id in TREE_BLOCKS:
                    editor.placeBlock((x + dx, cy, z + dz), Block("air"))

def build_migrant_cabin(editor, world_slice, house_data):
    
    from villages.builder import get_height  

    base_x = house_data["x"]
    base_z = house_data["z"]
    
    
    width, length, height = 5, 6, 3
    
    
    base_y = get_height(world_slice, base_x, base_z)
    facing = house_data.get("facing", "north")

    
    roof_dir = {
        "north": {"left": "east", "right": "west"},
        "south": {"left": "west", "right": "east"},
        "east":  {"left": "south", "right": "north"},
        "west":  {"left": "north", "right": "south"}
    }
    
    
    placeCuboid(editor, (base_x - 1, base_y, base_z - 1), (base_x + width + 1, base_y + height + 4, base_z + length + 1), Block("air"))
    placeCuboid(editor, (base_x - 1, base_y - 1, base_z - 1), (base_x + width, base_y - 1, base_z + length), Block("cobblestone"))

    
    log_block = Block("oak_log", {"axis": "y"})
    for dy in range(height):
        for dx in range(width):
            for dz in range(length):
                if dx == 0 or dx == width - 1 or dz == 0 or dz == length - 1:
                    # Remplacement de IVec3 par un simple tuple (x, y, z)
                    editor.placeBlock((base_x + dx, base_y + dy, base_z + dz), log_block)

    
    door_x, door_z = base_x + 2, base_z
    editor.placeBlock((door_x, base_y, door_z), Block("air"))
    editor.placeBlock((door_x, base_y + 1, door_z), Block("air"))
    editor.placeBlock((door_x, base_y, door_z), Block("oak_door", {"half": "lower", "facing": facing}))
    editor.placeBlock((door_x, base_y + 1, door_z), Block("oak_door", {"half": "upper", "facing": facing}))

    editor.placeBlock((base_x, base_y + 1, base_z + 3), Block("glass_pane"))
    editor.placeBlock((base_x + width - 1, base_y + 1, base_z + 3), Block("glass_pane"))

    
    side_left = roof_dir[facing]["left"]
    side_right = roof_dir[facing]["right"]

    for dz in range(-1, length + 1):
        editor.placeBlock((base_x - 1, base_y + height, base_z + dz), Block("spruce_stairs", {"facing": side_left}))
        editor.placeBlock((base_x, base_y + height + 1, base_z + dz), Block("spruce_stairs", {"facing": side_left}))
        editor.placeBlock((base_x + width, base_y + height, base_z + dz), Block("spruce_stairs", {"facing": side_right}))
        editor.placeBlock((base_x + width - 1, base_y + height + 1, base_z + dz), Block("spruce_stairs", {"facing": side_right}))
        editor.placeBlock((base_x + 2, base_y + height + 2, base_z + dz), Block("spruce_slab", {"type": "bottom"}))

    
    for dx in range(1, width - 1):
        editor.placeBlock((base_x + dx, base_y + height, base_z), Block("oak_planks"))
        editor.placeBlock((base_x + dx, base_y + height, base_z + length - 1), Block("oak_planks"))
    editor.placeBlock((base_x + 2, base_y + height + 1, base_z), Block("oak_planks"))
    editor.placeBlock((base_x + 2, base_y + height + 1, base_z + length - 1), Block("oak_planks"))


def build_house(editor, world_slice, house):
    if house.get("style") == "cabin":
        build_migrant_cabin(editor, world_slice, house)

    x = house["x"]
    z = house["z"]

    mat = get_materials(house["resource"])

    wall_name         = pick(mat["wall"])
    log_name          = pick(mat["log"])
    slab_name         = pick(mat["slab"])
    stair_name        = pick(mat["stairs"])
    glass_name        = mat["glass"]
    floor_name        = mat["floor"]
    floor_inside_name = pick(mat["floor_inside"])
    door_name         = mat["door"]
    light_name        = mat["light"]

    wall_block         = Block(wall_name)
    log_block          = Block(log_name)
    glass_block        = Block(glass_name)
    floor_block        = Block(floor_name)
    floor_inside_block = Block(floor_inside_name)

    width  = randint(5, 8)
    depth  = randint(5, 8)
    height = randint(4, 5)

    orientation = choice(["north", "south", "east", "west"])

    y = _ground_level(world_slice, x, z, width, depth) - 1
    house["y"] = y
    house["width"] = width
    house["depth"] = depth

    house["placed_improvements"] = []
    house["used_positions"] = []

    _clear_trees(editor, world_slice, x, z, width, depth, y)
    _fill_foundation(editor, world_slice, x, z, width, depth, y, wall_block)

    # Fondation
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

    # Empty the inside
    placeCuboid(
        editor,
        (x + 1,         y + 1,          z + 1),
        (x + width - 1, y + height - 1, z + depth - 1),
        Block("air")
    )

    # floor
    place_floor(editor, x, y, z, width, depth, floor_inside_block)

    # Corner Beam
    for cx, cz in [
        (x,          z),
        (x + width,  z),
        (x,          z + depth),
        (x + width,  z + depth),
    ]:
        for dy in range(1, height):
            editor.placeBlock((cx, y + dy, cz), log_block)

    # Windows
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

    # Roof
    build_roof(
        editor,
        x, y + height, z,
        width, depth,
        orientation,
        stair_name, slab_name,
        log_name
    )

    # Door
    place_door(
        editor,
        x, y, z,
        width, depth,
        orientation,
        door_name
    )

    # Light
    editor.placeBlock(
        (x + width // 2, y + height - 1, z + depth // 2),
        Block(light_name)
    )

def improve_house(editor, house):

    x = house["x"]
    z = house["z"]

    width = house["width"]
    depth = house["depth"]
    y = house["y"]

    resource = house["resource"]


    available = improvements.get(
        resource,
        ["crafting_table"]
    )

    current = house.get(
        "placed_improvements",
        []
    )

    remaining = [
        block
        for block in available
        if block not in current
    ]

    if not remaining:
        return None

    block_name = choice(remaining)

    positions = [
        (x + 1, y + 1, z + 1),
        (x + width - 1, y + 1, z + 1),
        (x + 1, y + 1, z + depth - 1),
        (x + width - 1, y + 1, z + depth - 1),
        (x + width // 2, y + 1, z + depth // 2)
    ]

    used_positions = house.get(
        "used_positions",
        []
    )

    free_positions = [
        pos
        for pos in positions
        if pos not in used_positions
    ]

    if not free_positions:
        return None

    pos = choice(free_positions)

    editor.placeBlock(
        pos,
        Block(block_name)
    )

    current.append(block_name)
    used_positions.append(pos)

    house["placed_improvements"] = current
    house["used_positions"] = used_positions

    return block_name