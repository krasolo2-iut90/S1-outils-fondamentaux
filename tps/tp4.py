# ================================================================================
# Exercice 1
# ================================================================================

def transposee(A):
    """Transposée de la matrice A, donnée comme liste de lignes."""
    lignes = len(A)
    colonnes = len(A[0])
    return [[A[i][j] for i in range(lignes)] for j in range(colonnes)]

print(transposee([[1, 2, 3], [4, 5, 6]]))

# ================================================================================
# Exercice 2
# ================================================================================

def produit(A, B):
    """Produit matriciel A x B, en Python pur."""
    n, p = len(A), len(A[0])
    if len(B) != p:
        raise ValueError("dimensions incompatibles")
    q = len(B[0])
    C = [[0] * q for _ in range(n)]
    for i in range(n):
        for j in range(q):
            somme = 0
            for k in range(p):
                somme = somme + A[i][k] * B[k][j]
            C[i][j] = somme
    return C

identite = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
print(produit(A, identite) == A)
print(produit([[1, 2], [3, 4]], [[0, 1], [1, 0]]))
# ================================================================================
import random
import time

random.seed(42)

def matrice_aleatoire(n):
    return [[random.random() for _ in range(n)] for _ in range(n)]

for n in (40, 80, 120):
    A = matrice_aleatoire(n)
    B = matrice_aleatoire(n)
    debut = time.perf_counter()
    produit(A, B)
    print(f"n = {n:>3} : {time.perf_counter() - debut:.4f} s")

# ================================================================================
# Exercice 3
# ================================================================================

import numpy as np

A = np.array([[1.0, 2.0, 2.0],
              [1.0, 3.0, -2.0],
              [3.0, 5.0, 8.0]])
b = np.array([2.0, -1.0, 8.0])

print(A.shape)
print(A.T)          # transposée
print(A @ A)        # produit matriciel
print(A * A)        # produit terme à terme : ce n'est PAS le produit matriciel

n = 120
A = matrice_aleatoire(n)
B = matrice_aleatoire(n)

debut = time.perf_counter()
produit(A, B)
t_python = time.perf_counter() - debut

An, Bn = np.array(A), np.array(B)
debut = time.perf_counter()
An @ Bn
t_numpy = time.perf_counter() - debut

print(f"python pur {t_python:.4f} s")
print(f"numpy      {t_numpy:.6f} s")
print("rapport :", round(t_python / max(t_numpy, 1e-9)))

# ================================================================================
# Exercice 4
# ================================================================================

def resoudre(A, b, tolerance=1e-14):
    """Résout A x = b par le pivot de Gauss avec pivot partiel.

    A est une liste de lignes, b une liste. Ni A ni b ne sont modifiés.
    Un pivot inférieur ou égal à tolerance est considéré comme nul.
    """
    n = len(A)
    # copie de travail, matrice augmentée [A | b]
    M = [list(A[i]) + [b[i]] for i in range(n)]

    for k in range(n):
        # pivot partiel : la ligne dont le coefficient est le plus grand en valeur absolue
        meilleure = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[meilleure][k]) <= tolerance:
            raise ValueError("systeme singulier ou mal pose")
        M[k], M[meilleure] = M[meilleure], M[k]

        # élimination sous la diagonale
        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] = M[i][j] - facteur * M[k][j]

    # remontée : on résout de la dernière équation vers la première
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        somme = M[i][n]
        for j in range(i + 1, n):
            somme = somme - M[i][j] * x[j]
        x[i] = somme / M[i][i]
    return x

A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
b = [2, -1, 8]
x = resoudre(A, b)
print([round(v, 10) for v in x])

# vérification : A x doit redonner b
verif = [sum(A[i][j] * x[j] for j in range(3)) for i in range(3)]
print([round(v, 10) for v in verif])
# ================================================================================
random.seed(7)
n = 50
A = matrice_aleatoire(n)
b = [random.random() for _ in range(n)]

mienne = resoudre(A, b)
celle_de_numpy = np.linalg.solve(np.array(A), np.array(b))

ecart = max(abs(mienne[i] - celle_de_numpy[i]) for i in range(n))
print("ecart maximal :", ecart)
print(ecart < 1e-9)

# ================================================================================
# Exercice 5
# ================================================================================

def hilbert(n):
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])

n = 12
H = hilbert(n)
x_vrai = np.ones(n)          # on choisit la solution d'avance
b = H @ x_vrai               # et on fabrique le second membre correspondant

x_solve = np.linalg.solve(H, b)
x_inverse = np.linalg.inv(H) @ b

print("erreur avec solve   :", float(np.max(np.abs(x_solve - x_vrai))))
print("erreur avec inv @ b :", float(np.max(np.abs(x_inverse - x_vrai))))
print("conditionnement     : {:.3e}".format(float(np.linalg.cond(H))))

# ================================================================================
# Exercice 6
# ================================================================================

import matplotlib.pyplot as plt

def rotation(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s], [s, c]])

# une maison, comme suite de points (fermée)
maison = np.array([[0, 0], [2, 0], [2, 1.5], [1, 2.5], [0, 1.5], [0, 0]]).T

plt.figure(figsize=(5, 5))
plt.plot(maison[0], maison[1], label="depart")
for angle in (np.pi / 6, np.pi / 3, np.pi / 2):
    image = rotation(angle) @ maison
    plt.plot(image[0], image[1], label=f"rotation {int(np.degrees(angle))} degres")
plt.axis("equal")
plt.legend()
plt.title("Une matrice fait tourner une figure")
plt.show()

gauche = rotation(np.pi / 3) @ rotation(np.pi / 6)
droite = rotation(np.pi / 2)
print(np.allclose(gauche, droite))
print(np.round(droite, 10))

# ================================================================================
# Exercice 7
# ================================================================================

def determinant(A):
    """Déterminant de A par élimination de Gauss avec pivot partiel."""
    n = len(A)
    M = [list(ligne) for ligne in A]
    det = 1.0
    for k in range(n):
        meilleure = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[meilleure][k]) < 1e-14:
            return 0.0
        if meilleure != k:
            M[k], M[meilleure] = M[meilleure], M[k]
            det = -det
        det = det * M[k][k]
        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] = M[i][j] - facteur * M[k][j]
    return det

A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
print(determinant(A), float(np.linalg.det(np.array(A, dtype=float))))
print(determinant([[1, 2], [2, 4]]))

# ================================================================================
# Exercice 8
# ================================================================================

from fractions import Fraction

def hilbert_exacte(n):
    return [[Fraction(1, i + j + 1) for j in range(n)] for i in range(n)]

n = 12
H_exacte = hilbert_exacte(n)
b_exact = [sum(ligne) for ligne in H_exacte]

try:
    resoudre(H_exacte, b_exact)
except ValueError as erreur:
    print("premier essai :", erreur)

x_exact = resoudre(H_exacte, b_exact, tolerance=0)
print(x_exact)
print(all(v == 1 for v in x_exact))

# ================================================================================
#
# ================================================================================