from houses import generate_houses
from houses import build_house

from agents import generate_agents
from agents import build_agent


RESOURCE_VILLAGE_SIZE = {
    "wood": 8,
    "food": 6,
    "stone": 4,
    "sand": 3,
    "basic": 2
}


def create_villages(zones):

    villages = []

    for zone in zones:

        size = RESOURCE_VILLAGE_SIZE[
            zone["resource"]
        ]

        village = {
            "x": zone["x"],
            "z": zone["z"],
            "biome": zone["biome"],
            "resource": zone["resource"],
            "houses": [],
            "agents": []
        }

        village["houses"] = generate_houses(
            village,
            size
        )

        village["agents"] = generate_agents(
            village["houses"]
        )

        villages.append(village)

    return villages


def build_village(editor, world_slice, village):

    for house in village["houses"]:

        build_house(
            editor,
            world_slice,
            house
        )

    for agent in village["agents"]:

        build_agent(
            editor,
            world_slice,
            agent
        )