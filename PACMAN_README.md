# Pacman - Jeu Simple

Un jeu Pacman simple implémenté en Python avec Pygame.

## Installation

```bash
pip install -r requirements.txt
```

## Lancer le jeu

```bash
python src/pacman.py
```

## Comment jouer

- **Flèches du clavier** : Déplacer Pacman (↑ ↓ ← →)
- **Objectif** : Manger tous les petits points (pellets)
- **Éviter** : Les trois fantômes qui se déplacent aléatoirement
- **Score** : +10 points par pellet mangé

## Caractéristiques

- **Labyrinthe généré aléatoirement** : Chaque partie a une map unique
- **Trois fantômes** : Différentes couleurs avec IA simple
- **Pellets** : À manger pour augmenter votre score
- **Collision** : Le jeu s'arrête si Pacman touche un fantôme

## Contrôles

| Touche | Action |
|--------|--------|
| ↑ | Aller vers le haut |
| ↓ | Aller vers le bas |
| ← | Aller à gauche |
| → | Aller à droite |
| Fermer | Quitter le jeu |

## Mécanique du Jeu

- Pacman se déplace rapidement
- Les fantômes se déplacent plus lentement et aléatoirement
- Les pellets disparaissent quand Pacman passe dessus
- Le score s'affiche en haut à gauche
