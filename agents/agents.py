from gdpc import Block

from villages.builder import get_height
from agents.behaviour import decide


def create_agent(house, village, index):

    return {
        "name":             f"agent_{index}",
        "house":            house,
        "village":          village,
        "resource":         house["resource"],
        "inventory":        {house["resource"]: 1},
        "migrate_cooldown": 0,
        "improved":         0,
        "history":          [],
    }


def generate_agents(village):

    agents = []

    for i, house in enumerate(village["houses"]):

        agent = create_agent(house, village, i)

        house["owner"] = agent["name"]

        agents.append(agent)

    return agents


def build_agent(editor, world_slice, agent):

    x = agent["house"]["x"] + 2
    z = agent["house"]["z"] + 2

    y = get_height(world_slice, x, z)

    editor.placeBlock(
        (x, y, z),
        Block("emerald_block")
    )


def tick_agent(agent, all_villages, editor, world_slice):

    if agent["migrate_cooldown"] > 0:
        agent["migrate_cooldown"] -= 1

    action = decide(agent, all_villages)

    if action["type"] == "migrate":
        _migrate(agent, action["target"], editor, world_slice)

    elif action["type"] == "improve":
        _improve(agent, editor, world_slice)

    else:
        _idle(agent)

    agent["history"].append(action["type"])


def _migrate(agent, target_village, editor, world_slice):

    from villages.houses.houses import build_house
    from villages.houses.houses_data import create_house

    current = agent["village"]

    current["agents"].remove(agent)
    current["resources"][agent["resource"]] = max(
        0,
        current["resources"].get(agent["resource"], 0) - 1
    )

    target_village["resources"][agent["resource"]] = (
        target_village["resources"].get(agent["resource"], 0) + 1
    )

    target_res = target_village["resource"]
    agent["inventory"][target_res] = (
        agent["inventory"].get(target_res, 0) + 1
    )

    new_house = create_house(
        target_village["x"] + 8,
        target_village["z"] + 8,
        target_village["biome"],
        target_village["resource"],
    )
    new_house["owner"] = agent["name"]

    build_house(editor, world_slice, new_house)
    target_village["houses"].append(new_house)
    target_village["agents"].append(agent)

    agent["house"]   = new_house
    agent["village"] = target_village
    agent["migrate_cooldown"] = 3


def _improve(agent, editor, world_slice):

    x = agent["house"]["x"] + 2
    z = agent["house"]["z"] + 2

    y = get_height(world_slice, x, z)

    editor.placeBlock(
        (x, y + 5, z),
        Block("lantern")
    )

    agent["improved"] += 1


def _idle(agent):

    agent["inventory"][agent["resource"]] = (
        agent["inventory"].get(agent["resource"], 0) + 0.5
    )