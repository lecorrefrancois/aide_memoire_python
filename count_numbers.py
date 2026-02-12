"""Compte et affiche les nombres de 1 à 10."""


def count_numbers(start: int = 1, end: int = 10) -> None:
    """Affiche chaque nombre de start à end inclus.

    Args:
        start: Nombre de départ (défaut: 1).
        end: Nombre de fin inclus (défaut: 10).
    """
    for number in range(start, end + 1):
        print(number)


if __name__ == "__main__":
    count_numbers()
