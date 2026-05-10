from agent import get_zone, get_neighbors, compute_density

def step_simulation(agents, grid, config):
    alive_agents = []

    for agent in agents:
        agent["food"] -= config.FOOD_CONSUMPTION

        current_zone = get_zone(agent["x"], agent["z"], config.GRID_SIZE)
        neighbors = get_neighbors(current_zone, config.GRID_SIZE)

        best_zone = current_zone
        best_score = -1

        for zone in neighbors:
            if zone in grid:
                density = compute_density(agents, zone, config.GRID_SIZE)
                score = grid[zone] - density * config.DENSITY_WEIGHT

                if score > best_score:
                    best_score = score
                    best_zone = zone

        # déplacement
        import random
        agent["x"] = best_zone[0] + random.randint(0, config.GRID_SIZE - 1)
        agent["z"] = best_zone[1] + random.randint(0, config.GRID_SIZE - 1)

        # gain de nourriture
        agent["food"] += grid[current_zone] * config.FOOD_GAIN_FACTOR

        if agent["food"] > 0:
            alive_agents.append(agent)

    return alive_agents