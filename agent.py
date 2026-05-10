import random

def create_agents(num_agents, world_size):
    agents = []

    for _ in range(num_agents):
        agents.append({
            "x": random.randint(0, world_size),
            "z": random.randint(0, world_size),
            "food": 10
        })

    return agents


def get_zone(x, z, grid_size):
    gx = (x // grid_size) * grid_size
    gz = (z // grid_size) * grid_size
    return (gx, gz)


def get_neighbors(zone, grid_size):
    x, z = zone
    return [
        (x, z),
        (x + grid_size, z),
        (x - grid_size, z),
        (x, z + grid_size),
        (x, z - grid_size)
    ]


def compute_density(agents, zone, grid_size):
    count = 0
    for a in agents:
        if get_zone(a["x"], a["z"], grid_size) == zone:
            count += 1
    return count