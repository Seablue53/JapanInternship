from gdpc import Block

from builder import get_height


def create_agent(house, index):

    return {
        "name": f"agent_{index}",
        "x": house["x"],
        "z": house["z"],
        "house": house,
        "resource": house["resource"]
    }


def generate_agents(houses):

    agents = []

    for i, house in enumerate(houses):

        agent = create_agent(house, i)

        house["owner"] = agent["name"]

        agents.append(agent)

    return agents


def build_agent(editor, world_slice, agent):

    x = agent["x"] + 2
    z = agent["z"] + 2

    y = get_height(world_slice, x, z)

    editor.placeBlock(
        (x, y, z),
        Block("emerald_block")
    )