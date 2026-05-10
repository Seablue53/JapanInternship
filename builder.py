from gdpc import Block


def build_house(editor, x, y, z, material):

    # sol
    for dx in range(5):
        for dz in range(5):
            editor.placeBlock((x + dx, y, z + dz), Block(material))

    # murs
    for dy in range(1, 4):

        for dx in range(5):
            editor.placeBlock((x + dx, y + dy, z), Block(material))
            editor.placeBlock((x + dx, y + dy, z + 4), Block(material))

        for dz in range(5):
            editor.placeBlock((x, y + dy, z + dz), Block(material))
            editor.placeBlock((x + 4, y + dy, z + dz), Block(material))

    # toit
    for dx in range(5):
        for dz in range(5):
            editor.placeBlock((x + dx, y + 4, z + dz), Block(material))


def build_agent(editor, x, y, z):

    editor.placeBlock((x, y, z), Block("emerald_block"))


def get_material(resource):

    if resource == "wood":
        return "oak_planks"

    elif resource == "stone":
        return "stone_bricks"

    elif resource == "sand":
        return "sandstone"

    return "oak_planks"


def get_height(world_slice, x, z):

    return world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][x, z]


def build_village(editor, world_slice, village):

    for house in village["houses"]:

        material = get_material(house["resource"])

        x = house["x"]
        z = house["z"]

        y = get_height(world_slice, x, z)

        build_house(editor, x, y, z, material)

    for agent in village["agents"]:

        x = agent["x"] + 2
        z = agent["z"] + 2

        y = get_height(world_slice, x, z) + 1

        build_agent(editor, x, y, z)