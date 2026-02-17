"""Recuit simulé appliqué à la recherche du minimum de la surface 3D.

L'algorithme de recuit simulé (simulated annealing) est une métaheuristique
d'optimisation inspirée du processus de recuit en métallurgie : on chauffe
un matériau puis on le refroidit lentement pour atteindre un état d'énergie
minimale.

Principe :
    1. Partir d'un point aléatoire (x, y) et d'une température T élevée.
    2. À chaque itération, générer un voisin aléatoire.
    3. Si le voisin est meilleur (z plus bas), on l'accepte.
    4. Si le voisin est moins bon, on l'accepte quand même avec une
       probabilité exp(-delta / T). Cela permet d'échapper aux minima locaux.
    5. Réduire progressivement la température selon un schéma de
       refroidissement.
    6. Quand T est proche de 0, l'algorithme ne fait plus que descendre
       et converge vers un minimum.

Usage :
    python src/recuit_simule.py
"""

import numpy as np

from surface import GLOBAL_MIN_POS, X_BOUNDS, Y_BOUNDS, surface


def recuit_simule(
    t_init: float = 10.0,
    t_min: float = 1e-6,
    alpha: float = 0.995,
    max_iter_par_palier: int = 100,
    pas: float = 0.5,
    seed: int | None = None,
) -> dict:
    """Exécute le recuit simulé sur la surface.

    Args:
        t_init: Température initiale (plus elle est haute, plus
            l'exploration est large au début).
        t_min: Température d'arrêt (critère de fin).
        alpha: Facteur de refroidissement (0 < alpha < 1).
            La température est multipliée par alpha à chaque palier.
        max_iter_par_palier: Nombre de voisins testés à chaque palier
            de température.
        pas: Amplitude maximale du déplacement vers un voisin.
        seed: Graine aléatoire pour la reproductibilité.

    Returns:
        Dictionnaire contenant :
        - "x_best", "y_best", "z_best" : meilleur point trouvé
        - "historique" : liste de (x, y, z) à chaque étape acceptée
        - "temperatures" : liste des températures correspondantes
        - "n_acceptes" : nombre total de mouvements acceptés
        - "n_total" : nombre total de mouvements évalués
    """
    rng = np.random.default_rng(seed)

    # --- Point de départ aléatoire dans le domaine ---
    x = rng.uniform(X_BOUNDS[0], X_BOUNDS[1])
    y = rng.uniform(Y_BOUNDS[0], Y_BOUNDS[1])
    z = float(surface(x, y))

    # Meilleur point trouvé (global)
    x_best, y_best, z_best = x, y, z

    # Historique pour la visualisation
    historique: list[tuple[float, float, float]] = [(x, y, z)]
    temperatures: list[float] = [t_init]

    t = t_init
    n_acceptes = 0
    n_total = 0

    # --- Boucle principale ---
    while t > t_min:
        for _ in range(max_iter_par_palier):
            n_total += 1

            # Générer un voisin aléatoire
            x_voisin = x + rng.uniform(-pas, pas)
            y_voisin = y + rng.uniform(-pas, pas)

            # Contraindre au domaine
            x_voisin = np.clip(x_voisin, X_BOUNDS[0], X_BOUNDS[1])
            y_voisin = np.clip(y_voisin, Y_BOUNDS[0], Y_BOUNDS[1])

            z_voisin = float(surface(x_voisin, y_voisin))

            # Différence d'énergie
            delta = z_voisin - z

            # Critère d'acceptation de Metropolis
            if delta < 0 or rng.random() < np.exp(-delta / t):
                x, y, z = x_voisin, y_voisin, z_voisin
                n_acceptes += 1

                historique.append((x, y, z))
                temperatures.append(t)

                # Mettre à jour le meilleur si nécessaire
                if z < z_best:
                    x_best, y_best, z_best = x, y, z

        # Refroidissement
        t *= alpha

    return {
        "x_best": x_best,
        "y_best": y_best,
        "z_best": z_best,
        "historique": historique,
        "temperatures": temperatures,
        "n_acceptes": n_acceptes,
        "n_total": n_total,
    }


def main() -> None:
    """Lance le recuit simulé et affiche les résultats."""
    print("=" * 60)
    print("  RECUIT SIMULÉ — Recherche du minimum global")
    print("=" * 60)
    print()

    resultats = recuit_simule(
        t_init=10.0,
        t_min=1e-6,
        alpha=0.995,
        max_iter_par_palier=100,
        pas=0.5,
        seed=42,
    )

    x_b = resultats["x_best"]
    y_b = resultats["y_best"]
    z_b = resultats["z_best"]
    hist = resultats["historique"]

    print(f"Point de départ  : ({hist[0][0]:+.4f}, {hist[0][1]:+.4f})  "
          f"z = {hist[0][2]:.4f}")
    print(f"Minimum trouvé   : ({x_b:+.4f}, {y_b:+.4f})  z = {z_b:.4f}")
    print()

    gx, gy = GLOBAL_MIN_POS
    gz = float(surface(gx, gy))
    dist = np.sqrt((x_b - gx) ** 2 + (y_b - gy) ** 2)
    print(f"Minimum global   : ({gx:+.4f}, {gy:+.4f})  z = {gz:.4f}")
    print(f"Distance au global : {dist:.4f}")
    print()
    print(f"Mouvements acceptés : {resultats['n_acceptes']} / {resultats['n_total']}")
    print(f"Étapes enregistrées : {len(hist)}")


if __name__ == "__main__":
    main()
