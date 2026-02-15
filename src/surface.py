"""Surface 3D avec minima locaux et un minimum global.

Cette surface sert d'espace de test pour l'algorithme de recuit simule.
Elle combine une nappe ondulée (cosinus) avec des puits gaussiens de
profondeurs différentes, créant plusieurs minima locaux et un unique
minimum global.
"""

import numpy as np
from numpy.typing import ArrayLike


# ---------------------------------------------------------------------------
# Paramètres des puits gaussiens : (centre_x, centre_y, profondeur, largeur)
# Le puits le plus profond (profondeur = -6) constitue le minimum global.
# ---------------------------------------------------------------------------
WELLS: list[tuple[float, float, float, float]] = [
    # Minimum global
    (-2.0, 2.5, -6.0, 0.6),
    # Minima locaux
    (2.5, -1.5, -3.5, 0.5),
    (1.0, 3.0, -3.0, 0.7),
    (-3.0, -2.0, -2.5, 0.5),
    (3.5, 3.0, -2.0, 0.4),
    (-1.0, -3.5, -1.8, 0.6),
]

# Position connue du minimum global (pour vérification)
GLOBAL_MIN_POS: tuple[float, float] = (-2.0, 2.5)

# Domaine de recherche
X_BOUNDS: tuple[float, float] = (-5.0, 5.0)
Y_BOUNDS: tuple[float, float] = (-5.0, 5.0)


def surface(x: ArrayLike, y: ArrayLike) -> np.ndarray:
    """Calcule la valeur de la surface en (x, y).

    La surface est composée de :
    - une nappe ondulée de base : cos(x) * cos(y)
    - des puits gaussiens de profondeurs variées

    Args:
        x: Coordonnées en x (scalaire ou tableau numpy).
        y: Coordonnées en y (scalaire ou tableau numpy).

    Returns:
        Valeurs de la surface aux points (x, y).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # Nappe de base ondulée
    z = np.cos(x) * np.cos(y)

    # Ajout des puits gaussiens
    for cx, cy, depth, width in WELLS:
        z = z + depth * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * width**2))

    return z


def make_grid(
    n_points: int = 300,
    x_bounds: tuple[float, float] = X_BOUNDS,
    y_bounds: tuple[float, float] = Y_BOUNDS,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Génère une grille 2D et les valeurs de surface correspondantes.

    Args:
        n_points: Nombre de points par axe.
        x_bounds: Bornes de l'axe x (min, max).
        y_bounds: Bornes de l'axe y (min, max).

    Returns:
        Tuple (X, Y, Z) de tableaux 2D prêts pour le tracé.
    """
    x = np.linspace(x_bounds[0], x_bounds[1], n_points)
    y = np.linspace(y_bounds[0], y_bounds[1], n_points)
    X, Y = np.meshgrid(x, y)
    Z = surface(X, Y)
    return X, Y, Z
