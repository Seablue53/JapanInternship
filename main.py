from gdpc import Editor
import config
from map import build_grid
from agent import create_agents
from simulation import step_simulation

def main():
    editor = Editor(buffering=True)

    grid = build_grid(editor, config.WORLD_SIZE, config.GRID_SIZE)
    agents = create_agents(config.NUM_AGENTS, config.WORLD_SIZE)

    for step in range(config.STEPS):
        agents = step_simulation(agents, grid, config)
        print(f"Step {step}, agents restants: {len(agents)}")

if __name__ == "__main__":
    main()