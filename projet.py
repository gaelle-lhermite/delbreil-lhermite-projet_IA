from heapq import heappush, heappop

# --- Configuration du taquin ---
ETAT_OBJECTIF = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

DEPLACEMENTS = {
    'Haut': (-1, 0),
    'Bas': (1, 0),
    'Gauche': (0, -1),
    'Droite': (0, 1)
}

# --- Fonctions utilitaires ---

def lire_taquin():
    print("Entrez le taquin initial ligne par ligne (avec 0 pour la case vide) :")
    etat = []
    for i in range(3):
        ligne = list(map(int, input().split()))
        etat.append(tuple(ligne))
    return tuple(etat)


def trouver_vide(etat):
    for i in range(3):
        for j in range(3):
            if etat[i][j] == 0:
                return i, j


def deplacements_possibles(etat):
    """Retourne la liste des déplacements possibles à partir d'un état donné."""
    x, y = trouver_vide(etat)
    deplacements = []

    for move, (dx, dy) in DEPLACEMENTS.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [list(row) for row in etat]
            # Échange de la case vide avec la case cible
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            new_state_tuple = tuple(tuple(row) for row in new_state)
            deplacements.append((move, new_state_tuple))

    return deplacements


def heuristique(etat):
    """Heuristique : compte le nombre de tuiles mal placées."""
    mal_places = 0
    for i in range(3):
        for j in range(3):
            if etat[i][j] != 0 and etat[i][j] != ETAT_OBJECTIF[i][j]:
                mal_places += 1
    return mal_places

def heuristique_manhattan(etat):
    """Heuristique : somme des distances de Manhattan entre chaque tuile et sa position finale."""
    distance = 0
    for i in range(3):
        for j in range(3):
            valeur = etat[i][j]
            if valeur != 0:
                objectif_i = (valeur - 1) // 3
                objectif_j = (valeur - 1) % 3
                distance += abs(i - objectif_i) + abs(j - objectif_j)
    return distance

def heuristique_conflits_lineaires(etat):
    """Heuristique de Manhattan + conflits linéaires (admissible)."""
    manhattan = 0
    conflits = 0
    N = 3  # taille du taquin

    # --- Distance de Manhattan ---
    for i in range(N):
        for j in range(N):
            valeur = etat[i][j]
            if valeur != 0:
                objectif_i = (valeur - 1) // N
                objectif_j = (valeur - 1) % N
                manhattan += abs(i - objectif_i) + abs(j - objectif_j)

    # --- Conflits linéaires (lignes) ---
    for i in range(N):
        for j in range(N):
            valeur1 = etat[i][j]
            if valeur1 != 0 and (valeur1 - 1) // N == i:  # tuile à sa bonne ligne
                for k in range(j + 1, N):
                    valeur2 = etat[i][k]
                    if valeur2 != 0 and (valeur2 - 1) // N == i and valeur1 > valeur2:
                        conflits += 1

    # --- Conflits linéaires (colonnes) ---
    for j in range(N):
        for i in range(N):
            valeur1 = etat[i][j]
            if valeur1 != 0 and (valeur1 - 1) % N == j:  # tuile à sa bonne colonne
                for k in range(i + 1, N):
                    valeur2 = etat[k][j]
                    if valeur2 != 0 and (valeur2 - 1) % N == j and valeur1 > valeur2:
                        conflits += 1

    return manhattan + 2 * conflits


def afficher_taquin(etat):
    """Affiche joliment un état du taquin."""
    for i in range(3):
        ligne = ' '.join(str(x) if x != 0 else ' ' for x in etat[i])
        print(ligne)
    print("-------")


# --- Algorithme A* ---

def a_etoile(initial, heuristique_fonction):
    open_set = []
    heappush(open_set, (heuristique_fonction(initial), 0, initial, []))
    visited = set()

    while open_set:
        f, g, etat, chemin = heappop(open_set)

        if etat == ETAT_OBJECTIF:
            return chemin, etat, len(open_set), len(visited)

        if etat in visited:
            continue

        visited.add(etat)

        for move, next_state in deplacements_possibles(etat):
            if next_state not in visited:
                new_g = g + 1
                h = heuristique_fonction(next_state)
                heappush(open_set, (new_g + h, new_g, next_state, chemin + [(move, next_state)]))

    return None, None, 0, len(visited)


def main():
    initial = lire_taquin()
    print("\nRésolution en cours...\n")

    chemin, final, taille_open, taille_visited = a_etoile(initial,heuristique_conflits_lineaires)

    if chemin is None:
        print("Aucune solution trouvée.")
    else:
        print(f"Solution trouvée en {len(chemin)} coups :\n")
        etat_courant = initial
        afficher_taquin(etat_courant)

        for move, etat_suivant in chemin:
            print(f"Coup : {move} (heuristique = {heuristique_manhattan(etat_suivant)})")
            afficher_taquin(etat_suivant)
            etat_courant = etat_suivant

        print("🎯 Taquin résolu !")
        print(f"Nombre final d'états dans open : {taille_open}")
        print(f"Nombre d'états visités : {taille_visited}")


if __name__ == "__main__":
    main()