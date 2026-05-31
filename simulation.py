import time
from random import shuffle

from villages.village import build_village
from villages.village import tick_village
from stats import record_tick, plot


DEFAULT_TICKS      = 20
DEFAULT_TICK_DELAY = 1.0


def run(villages, editor, world_slice,
        ticks=DEFAULT_TICKS,
        tick_delay=DEFAULT_TICK_DELAY):

    # Construction initiale
    for village in villages:
        build_village(editor, world_slice, village)

    editor.flushBuffer()

    total_agents = sum(len(v["agents"]) for v in villages)
    print(f"\nSimulation : {len(villages)} villages, {total_agents} agents, {ticks} ticks\n")

    # Historique pour les graphiques
    history = {}

    for tick in range(ticks):

        print(f"── Tick {tick + 1}/{ticks} ──────────────────────")

        villages_this_tick = list(villages)
        shuffle(villages_this_tick)

        for village in villages_this_tick:
            tick_village(village, villages, editor, world_slice)

        editor.flushBuffer()

        record_tick(history, tick, villages)

        _print_state(villages)

        if tick_delay > 0:
            time.sleep(tick_delay)

    print("\nSimulation terminée.")
    _print_summary(villages)

    # Graphiques finaux
    plot(history, ticks)


def _print_state(villages):

    for v in villages:
        agents    = len(v.get("agents", []))
        resources = v.get("resources", {})
        biome     = v.get("biome", "?")
        resource  = v.get("resource", "?")

        res_str = ", ".join(
            f"{k}:{round(val, 1)}"
            for k, val in resources.items()
            if val > 0
        )

        print(
            f"  [{biome:10}] agents={agents:2}  "
            f"res={resource:6}  stocks=[{res_str}]"
        )


def _print_summary(villages):

    print("\n── Résumé final ──────────────────────────────────")

    for v in villages:

        biome     = v.get("biome", "?")
        resources = v.get("resources", {})
        agents    = v.get("agents", [])

        res_str = ", ".join(
            f"{k}:{round(val, 1)}"
            for k, val in resources.items()
        )

        print(f"\n  [{biome}]  agents={len(agents)}  stocks=[{res_str}]")

        for agent in agents:
            migrations   = agent["history"].count("migrate")
            improvements = agent["history"].count("improve")
            idle_count   = agent["history"].count("idle")
            inv_str      = ", ".join(
                f"{k}:{round(val, 1)}"
                for k, val in agent["inventory"].items()
            )
            print(
                f"    {agent['name']:20} "
                f"migré={migrations}x  "
                f"amélioré={improvements}x  "
                f"idle={idle_count}x  "
                f"inv=[{inv_str}]"
            )


import time
from stats import record_tick, plot


def run(villages, editor, world_slice,
        ticks=20,
        tick_delay=1.0):

    # Construction initiale
    for village in villages:
        build_village(editor, world_slice, village)

    editor.flushBuffer()

    total_agents = sum(len(v["agents"]) for v in villages)
    print(f"\nSimulation : {len(villages)} villages, {total_agents} agents, {ticks} ticks\n")

    history = {}

    for tick in range(ticks):

        print(f"── Tick {tick + 1}/{ticks} ──────────────────────")

        villages_this_tick = list(villages)
        shuffle(villages_this_tick)

        for village in villages_this_tick:
            tick_village(village, villages, editor, world_slice)

        editor.flushBuffer()

        record_tick(history, tick, villages)

        _print_state(villages)

        if tick_delay > 0:
            time.sleep(tick_delay)

    print("\nSimulation terminée.")
    plot(history, ticks)


def _print_state(villages):

    for v in villages:
        agents    = len(v.get("agents", []))
        resources = v.get("resources", {})
        biome     = v.get("biome", "?")
        resource  = v.get("resource", "?")

        res_str = ", ".join(
            f"{k}:{round(val, 1)}"
            for k, val in resources.items()
            if val > 0
        )

        print(
            f"  [{biome:10}] agents={agents:2}  "
            f"res={resource:6}  stocks=[{res_str}]"
        )