from gdpc import Editor

from grid import build_grid
from villages.village import create_villages
from simulation import run

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

    run(
        villages    = villages,
        editor      = editor,
        world_slice = world_slice,
        ticks       = config.SIMULATION_TICKS,
        tick_delay  = config.TICK_DELAY,
    )


if __name__ == "__main__":
    main()