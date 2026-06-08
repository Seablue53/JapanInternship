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

    from gdpc.block import Block
    from random import randint, choice
    from villages.builder import get_height

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

    test_x = target_village["x"] + 8
    test_z = target_village["z"] + 8

    new_house = {
        "x": test_x,
        "z": test_z,
        "biome": target_village["biome"],
        "resource": target_village["resource"],
        "owner": agent["name"],
        "style": "marker",
        "width": 1,
        "length": 1,
        "depth": 1
    }

    test_y = get_height(world_slice, test_x, test_z)
    
    editor.placeBlock((test_x, test_y, test_z), Block("emerald_block"))
    editor.placeBlock((test_x, test_y + 1, test_z), Block("red_banner"))

    target_village["houses"].append(new_house)
    target_village["agents"].append(agent)

    agent["house"]   = new_house
    agent["village"] = target_village
    agent["migrate_cooldown"] = 3


def _improve(agent, editor, world_slice):
    if agent.get("house") and agent["house"].get("style") == "marker":
        return

    from villages.houses.houses import improve_house

    house = agent["house"]

    improvement = improve_house(
        editor,
        house
    )

    if improvement is not None:

        agent["improved"] += 1

        print(
            f"{agent['name']} added {improvement}"
        )


def _idle(agent):

    agent["inventory"][agent["resource"]] = (
        agent["inventory"].get(agent["resource"], 0) + 0.5
    )