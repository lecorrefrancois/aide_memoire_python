"""Visualisation 3D de la surface de test pour le recuit simulé.

Génère deux vues complémentaires :
- une surface 3D interactive
- une carte de chaleur 2D (vue de dessus) avec les minima annotés

Usage :
    python src/visualize_surface.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from surface import GLOBAL_MIN_POS, WELLS, make_grid, surface


def plot_3d(X: np.ndarray, Y: np.ndarray, Z: np.ndarray) -> None:
    """Affiche la surface en 3D."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.85, edgecolor="none")

    # Marquer le minimum global
    gx, gy = GLOBAL_MIN_POS
    gz = float(surface(gx, gy))
    ax.scatter(gx, gy, gz, color="red", s=100, zorder=5, label="Minimum global")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x, y)")
    ax.set_title("Surface 3D — Espace de test pour le recuit simulé")
    ax.legend()
    plt.tight_layout()


def plot_heatmap(X: np.ndarray, Y: np.ndarray, Z: np.ndarray) -> None:
    """Affiche une carte de chaleur 2D avec les positions des minima."""
    fig, ax = plt.subplots(figsize=(10, 8))

    contour = ax.contourf(X, Y, Z, levels=60, cmap=cm.viridis)
    fig.colorbar(contour, ax=ax, label="f(x, y)")

    # Tracer les lignes de niveau
    ax.contour(X, Y, Z, levels=20, colors="white", linewidths=0.3, alpha=0.5)

    # Annoter chaque puits
    for i, (cx, cy, depth, _) in enumerate(WELLS):
        is_global = (cx, cy) == GLOBAL_MIN_POS
        color = "red" if is_global else "white"
        label = f"Global (z={depth:.1f})" if is_global else f"Local (z={depth:.1f})"
        ax.plot(cx, cy, "o", color=color, markersize=8, markeredgecolor="black")
        ax.annotate(
            label,
            (cx, cy),
            textcoords="offset points",
            xytext=(10, 10),
            fontsize=8,
            color=color,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc="black", alpha=0.6),
        )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Carte de chaleur — Minima locaux et minimum global")
    plt.tight_layout()


def main() -> None:
    """Point d'entrée : génère et affiche les deux visualisations."""
    X, Y, Z = make_grid(n_points=300)

    print("Surface générée :")
    print(f"  Domaine x : [{X.min():.1f}, {X.max():.1f}]")
    print(f"  Domaine y : [{Y.min():.1f}, {Y.max():.1f}]")
    print(f"  z min = {Z.min():.4f}, z max = {Z.max():.4f}")
    print(f"  Minimum global attendu en {GLOBAL_MIN_POS}")

    gx, gy = GLOBAL_MIN_POS
    print(f"  f({gx}, {gy}) = {float(surface(gx, gy)):.4f}")
    print()
    print("Puits configurés :")
    for i, (cx, cy, depth, width) in enumerate(WELLS):
        tag = " ← GLOBAL" if (cx, cy) == GLOBAL_MIN_POS else ""
        print(f"  [{i}] centre=({cx:+.1f}, {cy:+.1f}), "
              f"profondeur={depth:.1f}, largeur={width:.1f}{tag}")

    plot_3d(X, Y, Z)
    plot_heatmap(X, Y, Z)
    plt.show()


if __name__ == "__main__":
    main()
