from gdpc import Block


def place_door(editor, x, y, z, width, depth, orientation, door_name):
    """
    Place une porte vanilla (2 blocs de haut).

    Dégage l'ouverture dans le mur, puis pose
    le bloc lower et le bloc upper avec le bon facing.
    """

    facing_map = {
        "north": "north",
        "south": "south",
        "east":  "east",
        "west":  "west",
    }

    facing = facing_map[orientation]

    if orientation == "north":
        dx, dz = width // 2, 0

    elif orientation == "south":
        dx, dz = width // 2, depth

    elif orientation == "east":
        dx, dz = width, depth // 2

    else:  # west
        dx, dz = 0, depth // 2

    door_x = x + dx
    door_z = z + dz
    door_y = y + 1

    # Dégager l'ouverture (2 blocs de haut)
    editor.placeBlock((door_x, door_y,     door_z), Block("air"))
    editor.placeBlock((door_x, door_y + 1, door_z), Block("air"))

    # Partie basse
    editor.placeBlock(
        (door_x, door_y, door_z),
        Block(door_name, {"facing": facing, "half": "lower", "hinge": "left"})
    )

    # Partie haute
    editor.placeBlock(
        (door_x, door_y + 1, door_z),
        Block(door_name, {"facing": facing, "half": "upper", "hinge": "left"})
    )