from gdpc import Block

def _place_roof_ns(editor, x, base_y, z, width, depth, stair_name, slab_name, log_name):
    """Toit nord/sud : pignon sur X, faîtage parallèle à Z."""
    half = width // 2

    for layer in range(half + 1):
        lx = x + layer
        rx = x + width - layer
        ry = base_y + layer

        # Logs du pignon
        for pz in (z, z + depth):
            if lx <= rx:
                editor.placeBlock((lx, ry, pz), Block(log_name))
                if lx < rx:
                    editor.placeBlock((rx, ry, pz), Block(log_name))

        # Remplissage du toit
        for dz in range(depth + 1):
            curr_z = z + dz
            if lx < rx:
                # Escaliers qui se rejoignent pour largeur paire
                editor.placeBlock((lx, ry, curr_z), Block(stair_name, {"facing": "east"}))
                editor.placeBlock((rx, ry, curr_z), Block(stair_name, {"facing": "west"}))
            elif lx == rx:
                # LARGEUR IMPAIRE : On met un bloc plein au lieu d'une slab
                # On utilise log_name ou n'importe quel bloc plein (ex: 'spruce_planks')
                editor.placeBlock((lx, ry, curr_z), Block(log_name))

def _place_roof_ew(editor, x, base_y, z, width, depth, stair_name, slab_name, log_name):
    """Toit est/ouest : pignon sur Z, faîtage parallèle à X."""
    half = depth // 2

    for layer in range(half + 1):
        fz = z + layer
        bz = z + depth - layer
        ry = base_y + layer

        for px in (x, x + width):
            if fz <= bz:
                editor.placeBlock((px, ry, fz), Block(log_name))
                if fz < bz:
                    editor.placeBlock((px, ry, bz), Block(log_name))

        for dx in range(width + 1):
            curr_x = x + dx
            if fz < bz:
                editor.placeBlock((curr_x, ry, fz), Block(stair_name, {"facing": "south"}))
                editor.placeBlock((curr_x, ry, bz), Block(stair_name, {"facing": "north"}))
            elif fz == bz:
                # PROFONDEUR IMPAIRE : Bloc plein au sommet
                editor.placeBlock((curr_x, ry, fz), Block(log_name))

def build_roof(editor, x, base_y, z, width, depth, orientation,
               stair_name, slab_name, log_name):
    if orientation in ("north", "south"):
        _place_roof_ns(editor, x, base_y, z, width, depth, stair_name, slab_name, log_name)
    else:
        _place_roof_ew(editor, x, base_y, z, width, depth, stair_name, slab_name, log_name)