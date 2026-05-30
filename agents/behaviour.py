from random import random


# ── Probabilités de base ──────────────────────────────────────────────────────

P_MIGRATE = 0.20
P_IMPROVE = 0.25
# P_IDLE  = 0.55


# ── Décision principale ───────────────────────────────────────────────────────

def decide(agent, all_villages):
    """
    Retourne un dict action :
      {"type": "migrate", "target": village}
      {"type": "improve", "target": None}
      {"type": "idle",    "target": None}
    """

    p_migrate = _adjusted_migrate(agent, all_villages)
    p_improve = _adjusted_improve(agent)

    roll = random()

    if roll < p_migrate:

        target = _pick_target(agent, all_villages)

        if target is None:
            return {"type": "idle", "target": None}

        return {"type": "migrate", "target": target}

    elif roll < p_migrate + p_improve:
        return {"type": "improve", "target": None}

    return {"type": "idle", "target": None}


# ── Ajustements ───────────────────────────────────────────────────────────────

def _adjusted_migrate(agent, all_villages):

    if agent["migrate_cooldown"] > 0:
        return 0.0

    p = P_MIGRATE

    village_resources = agent["village"].get("resources", {})
    diversity = len([v for v in village_resources.values() if v > 0])

    if diversity <= 1:
        p += 0.15   # village mono-ressource → fort besoin d'échange
    elif diversity >= 3:
        p -= 0.10   # village diversifié → moins besoin de partir

    total_inventory = sum(agent["inventory"].values())
    if total_inventory < 2:
        p += 0.10   # inventaire pauvre → cherche d'autres ressources

    return max(0.0, min(1.0, p))


def _adjusted_improve(agent):

    p = P_IMPROVE

    village_resources = agent["village"].get("resources", {})
    total_resources = sum(village_resources.values())

    if total_resources >= 5:
        p += 0.15   # village riche → on améliore

    if agent["improved"] == 0:
        p += 0.05   # jamais améliorée → légère incitation

    return max(0.0, min(1.0, p))


# ── Sélection de la destination ───────────────────────────────────────────────

def _pick_target(agent, all_villages):

    current = agent["village"]

    candidates = [v for v in all_villages if v is not current]

    if not candidates:
        return None

    # Préférer les villages avec une ressource différente
    diverse = [
        v for v in candidates
        if v.get("resource") != current.get("resource")
    ]

    pool = diverse if diverse else candidates

    return _weight_by_distance(current, pool)


def _weight_by_distance(origin, villages):
    """Tirage pondéré par distance inverse — villages proches favorisés."""

    if not villages:
        return None

    ox = origin.get("x", 0)
    oz = origin.get("z", 0)

    weights = []

    for v in villages:
        dx = v.get("x", 0) - ox
        dz = v.get("z", 0) - oz
        dist = max(1.0, (dx ** 2 + dz ** 2) ** 0.5)
        weights.append(1.0 / dist)

    total = sum(weights)
    roll  = random() * total
    cumul = 0.0

    for v, w in zip(villages, weights):
        cumul += w
        if roll <= cumul:
            return v

    return villages[-1]