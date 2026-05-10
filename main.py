from gdpc import Editor

from grid import build_grid

from village import create_villages
from village import build_village

import config


def main():

    editor = Editor(buffering=True)

    world_slice = editor.loadWorldSlice()

    zones = build_grid(
        editor,
        config.WORLD_SIZE,
        config.GRID_SIZE
    )

    villages = create_villages(zones)

    for village in villages:

        build_village(
            editor,
            world_slice,
            village
        )

    editor.flushBuffer()

    for village in villages:

        print(village)


if __name__ == "__main__":
    main()