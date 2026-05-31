import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def record_tick(history, tick, villages):
    """
    Enregistre l'état de tous les villages à un tick donné.
    À appeler à la fin de chaque tick dans simulation.py.
    """

    for village in villages:

        biome = village.get("biome", "?")

        if biome not in history:
            history[biome] = {
                "agents":    [],
                "resources": {},
            }

        history[biome]["agents"].append(
            len(village.get("agents", []))
        )

        for res, qty in village.get("resources", {}).items():

            if res not in history[biome]["resources"]:
                history[biome]["resources"][res] = []

            history[biome]["resources"][res].append(round(qty, 1))


def plot(history, ticks):
    """
    Génère deux graphiques :
      1. Évolution du nombre d'agents par village
      2. Évolution des stocks de ressources par village
    """

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Simulation ABM — Migrations et ressources", fontsize=14)

    _plot_agents(axes[0], history, ticks)
    _plot_resources(axes[1], history, ticks)

    plt.tight_layout()
    plt.savefig("simulation_results.png", dpi=150)
    plt.show()

    print("Graphique sauvegardé : simulation_results.png")


def _plot_agents(ax, history, ticks):

    ax.set_title("Agents par village")
    ax.set_xlabel("Tick")
    ax.set_ylabel("Nombre d'agents")

    x = list(range(1, ticks + 1))

    for biome, data in history.items():

        agents = data["agents"]

        if len(agents) < ticks:
            agents += [agents[-1]] * (ticks - len(agents))

        ax.plot(x, agents[:ticks], marker="o", markersize=3, label=biome)

    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)


def _plot_resources(ax, history, ticks):

    ax.set_title("Stocks de ressources par village")
    ax.set_xlabel("Tick")
    ax.set_ylabel("Quantité")

    x = list(range(1, ticks + 1))

    for biome, data in history.items():

        for res, quantities in data["resources"].items():

            if len(quantities) < ticks:
                quantities += [quantities[-1]] * (ticks - len(quantities))

            label = f"{biome} ({res})"
            ax.plot(x, quantities[:ticks], marker="s", markersize=3, label=label)

    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)