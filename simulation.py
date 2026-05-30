from random import randint, shuffle

from villages.houses.houses import generate_houses
from villages.houses.houses import build_house

from agents.agents import generate_agents
from agents.agents import build_agent
from agents.agents import tick_agent



def get_village_size(resource):

    if resource == "wood":
        return randint(12, 18)

    elif resource == "food":
        return randint(10, 16)

    elif resource == "stone":
        return randint(8, 14)

    elif resource == "sand":
        return randint(6, 10)

    return randint(5, 8)




def create_villages(zones):

    villages = []

    village_spacing = 100
    occupied_positions = []

    for zone in zones:

        if randint(0, 100) > 8:
            continue

        zx = zone["x"]
        zz = zone["z"]

        too_close = False

        for ox, oz in occupied_positions:

            distance = (
                (zx - ox) ** 2 +
                (zz - oz) ** 2
            ) ** 0.5

            if distance < village_spacing:
                too_close = True
                break

        if too_close:
            continue

        occupied_positions.append((zx, zz))

        size = get_village_size(zone["resource"])

        village = {
            "x":         zx,
            "z":         zz,
            "biome":     zone["biome"],
            "resource":  zone["resource"],
            "houses":    [],
            "agents":    [],
            "resources": {zone["resource"]: 3},  # stock initial
        }

        village["houses"] = generate_houses(village, size)
        village["agents"] = generate_agents(village)

        villages.append(village)

    return villages




def build_village(editor, world_slice, village):

    for house in village["houses"]:
        build_house(editor, world_slice, house)

    for agent in village["agents"]:
        build_agent(editor, world_slice, agent)



def tick_village(village, all_villages, editor, world_slice):
    """
    Fait jouer tous les agents du village pour un tick.
    L'ordre est mélangé pour éviter les biais de priorité.
    """

    agents_this_tick = list(village["agents"])
    shuffle(agents_this_tick)

    for agent in agents_this_tick:
        tick_agent(agent, all_villages, editor, world_slice)