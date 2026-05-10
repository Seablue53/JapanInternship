from gdpc import Block


def build_roof(editor, x, base_y, z, width, depth, orientation,
               stair_name, slab_name, log_name):
    """
    Toit en pignon (gable roof) façon vanilla.

    Gère correctement les largeurs/profondeurs paires ET impaires.

    Paire  (ex: width=6) → lx == rx à un moment → une slab au faîte
    Impaire (ex: width=7) → lx et rx se croisent sans jamais être égaux
                          → deux slabs adjacentes au faîte
    """

    if orientation in ("north", "south"):

        layers = (width // 2) + 1

        for layer in range(layers):

            lx = x + layer
            rx = x + width - layer
            ry = base_y + layer

            # Les deux côtés se sont croisés : cas impair déjà traité après
            if lx > rx:
                break

            for pz in (z, z + depth):
                if lx < rx:
                    editor.placeBlock((lx, ry, pz), Block(log_name))
                    editor.placeBlock((rx, ry, pz), Block(log_name))
                else:
                    editor.placeBlock((lx, ry, pz), Block(log_name))

            for dz in range(depth + 1):
                if lx < rx:
                    editor.placeBlock(
                        (lx, ry, z + dz),
                        Block(stair_name, {"facing": "east"})
                    )
                    editor.placeBlock(
                        (rx, ry, z + dz),
                        Block(stair_name, {"facing": "west"})
                    )
                else:
                    editor.placeBlock(
                        (lx, ry, z + dz),
                        Block(slab_name, {"type": "top"})
                    )

        # Largeur impaire : faîte double (deux slabs côte à côte)
        if width % 2 == 1:
            faite_layer = width // 2
            lx = x + faite_layer
            rx = lx + 1
            ry = base_y + faite_layer

            for pz in (z, z + depth):
                editor.placeBlock((lx, ry, pz), Block(log_name))
                editor.placeBlock((rx, ry, pz), Block(log_name))

            for dz in range(depth + 1):
                editor.placeBlock(
                    (lx, ry, z + dz),
                    Block(slab_name, {"type": "top"})
                )
                editor.placeBlock(
                    (rx, ry, z + dz),
                    Block(slab_name, {"type": "top"})
                )

    else:

        layers = (depth // 2) + 1

        for layer in range(layers):

            fz = z + layer
            bz = z + depth - layer
            ry = base_y + layer

            if fz > bz:
                break

            for px in (x, x + width):
                if fz < bz:
                    editor.placeBlock((px, ry, fz), Block(log_name))
                    editor.placeBlock((px, ry, bz), Block(log_name))
                else:
                    editor.placeBlock((px, ry, fz), Block(log_name))

            for dx in range(width + 1):
                if fz < bz:
                    editor.placeBlock(
                        (x + dx, ry, fz),
                        Block(stair_name, {"facing": "south"})
                    )
                    editor.placeBlock(
                        (x + dx, ry, bz),
                        Block(stair_name, {"facing": "north"})
                    )
                else:
                    editor.placeBlock(
                        (x + dx, ry, fz),
                        Block(slab_name, {"type": "top"})
                    )

        # Profondeur impaire : faîte double
        if depth % 2 == 1:
            faite_layer = depth // 2
            fz = z + faite_layer
            bz = fz + 1
            ry = base_y + faite_layer

            for px in (x, x + width):
                editor.placeBlock((px, ry, fz), Block(log_name))
                editor.placeBlock((px, ry, bz), Block(log_name))

            for dx in range(width + 1):
                editor.placeBlock(
                    (x + dx, ry, fz),
                    Block(slab_name, {"type": "top"})
                )
                editor.placeBlock(
                    (x + dx, ry, bz),
                    Block(slab_name, {"type": "top"})
                )