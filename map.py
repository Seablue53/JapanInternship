def get_resource_score(editor, x, z):
    biome = editor.getBiome((x, 0, z))

    if "plains" in biome:
        return 0.8
    elif "forest" in biome:
        return 0.9
    elif "desert" in biome:
        return 0.1
    else:
        return 0.5


def build_grid(editor, world_size, grid_size):
    grid = {}

    for gx in range(0, world_size, grid_size):
        for gz in range(0, world_size, grid_size):
            total = 0

            for x in range(gx, gx + grid_size):
                for z in range(gz, gz + grid_size):
                    total += get_resource_score(editor, x, z)

            avg = total / (grid_size * grid_size)
            grid[(gx, gz)] = avg

    return grid