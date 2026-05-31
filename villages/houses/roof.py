from gdpc import Block
from gdpc.geometry import placeCuboid


def _plank_from_stair(stair_name):
    return stair_name.replace("_stairs", "_planks")


def _place_roof_ns(editor, x, base_y, z, width, depth, stair_name, slab_name):
    """Pignon sur X, faîtage parallèle à Z. Déborde de 1 bloc sur les côtés."""
    middle     = width // 2
    plank_name = _plank_from_stair(stair_name)

    # On boucle sur la hauteur du toit
    for layer in range(middle + 1):
        yy = base_y + layer
        
        # On recule de 'layer' par rapport aux bords EXTÉRIEURS (qui incluent le débord de 1 bloc)
        # Maison va de x à x+width. Avec débord, le toit va de x-1 à x+width+1
        left_x  = (x - 1) + layer
        right_x = (x + width + 1) - layer

        if left_x < right_x:
            # Escalier gauche (tourné vers l'est pour monter vers le centre)
            placeCuboid(editor, (left_x, yy, z - 1), (left_x, yy, z + depth + 1), Block(stair_name, {"facing": "east"}))
            # Escalier droit (tourné vers l'ouest pour monter vers le centre)
            placeCuboid(editor, (right_x, yy, z - 1), (right_x, yy, z + depth + 1), Block(stair_name, {"facing": "west"}))

            # Remplissage en triangle plein (planches) entre les deux escaliers
            if left_x + 1 <= right_x - 1:
                placeCuboid(
                    editor,
                    (left_x + 1, yy, z - 1),
                    (right_x - 1, yy, z + depth + 1),
                    Block(plank_name)
                )
        else:
            # Faîte plat (si largeur paire)
            placeCuboid(editor, (left_x, yy, z - 1), (left_x, yy, z + depth + 1), Block(plank_name))

    # Faîte pointu (si largeur impaire) : on pose une dalle un bloc au-dessus
    if width % 2 == 1:
        # Le sommet se trouve pile au milieu : x + middle
        # Mais comme on a élargi le toit, il faut vérifier si le sommet nécessite une dalle
        # Avec notre calcul, si width est impair, le dernier layer left_x et right_x se croisent.
        # Pour finir proprement le toit avec la dalle :
        placeCuboid(
            editor,
            (x + middle, base_y + middle + 1, z - 1),
            (x + middle, base_y + middle + 1, z + depth + 1),
            Block(slab_name)
        )


def _place_roof_ew(editor, x, base_y, z, width, depth, stair_name, slab_name):
    """Pignon sur Z, faîtage parallèle à X. Déborde de 1 bloc sur les côtés."""
    middle     = depth // 2
    plank_name = _plank_from_stair(stair_name)

    for layer in range(middle + 1):
        yy = base_y + layer
        front_z = (z - 1) + layer
        back_z  = (z + depth + 1) - layer

        if front_z < back_z:
            # Escalier avant
            placeCuboid(editor, (x - 1, yy, front_z), (x + width + 1, yy, front_z), Block(stair_name, {"facing": "south"}))
            # Escalier arrière
            placeCuboid(editor, (x - 1, yy, back_z), (x + width + 1, yy, back_z), Block(stair_name, {"facing": "north"}))

            # Remplissage en planches
            if front_z + 1 <= back_z - 1:
                placeCuboid(
                    editor,
                    (x - 1, yy, front_z + 1),
                    (x + width + 1, yy, back_z - 1),
                    Block(plank_name)
                )
        else:
            placeCuboid(editor, (x - 1, yy, front_z), (x + width + 1, yy, front_z), Block(plank_name))

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