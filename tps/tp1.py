# --- Exercice 1.1 ---
q = 2026 // 7
r = 2026 % 7
print("quotient", q, ", reste", r)

# verification : quotient * diviseur + reste doit redonner le nombre de depart
print(289 * 7 + 3 == 2026)   # True

# --- Exercice 1.2 ---
dernier = 123456789 % 10
sans_dernier = 123456789 // 10
print(dernier)        # 9
print(sans_dernier)   # 12345678

# J'avais mis 123456789 / 10 au début et ça m'a donné 12345678.9, pas un entier. C'est le piège / contre // dont parle l'énoncé, je l'ai fait deux fois avant de comprendre.

# --- Exercice 2: ex ---
print(0.1 + 0.2)              # 0.30000000000000004
print(0.1 + 0.2 == 0.3)       # False

# --- Exercice 2.1 ---
s = 0.0
for i in range(1000):
    s = s + 0.1
print(s)                      # 99.9999999999986 ou tres proche
print(abs(s - 100))           # ~1.4e-12

# --- Exercice 2.2 ---
import math

def presque_egaux(a, b, tol=1e-9):
    """Renvoie True si a et b sont egaux a une tolerance relative pres."""
    return math.isclose(a, b, rel_tol=tol)

print(presque_egaux(0.1 + 0.2, 0.3))   # True
print(0.1 + 0.2 == 0.3)                # False

# J'ai demandé à un assistant une fonction qui teste si deux décimaux sont égaux. Première réponse : return a == b. C'était exactement le piège signalé dans le TP. Quand je lui ai demandé pourquoi une tolérance fixe de 1e-9 est mauvaise pour comparer des nombres de l'ordre de 1e20, il a répondu que 1e-9 devient négligeable devant 1e20 : deux nombres peuvent différer de millions d'unités et passer quand même pour « proches ». Inversement, pour des grandeurs de l'ordre de 1e-15, la même tolérance écrase tout et déclare égaux deux nombres très différents. D'où l'intérêt de math.isclose, qui raisonne en relatif plutôt qu'en absolu.

# --- Exercice 3.1 ---
for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")
    
# --- Exercice 3.2 ---
somme = 0
for n in range(1, 101):
    somme = somme + n
print(somme)          # 5050

n = 100
print(n * (n + 1) // 2)   # 5050

# J'ai utilisé // dans la formule parce qu'avec / j'obtenais 5050.0. La somme est bien un entier, autant garder un entier.

# --- Exercice 4.1 ---
def nombre_de_chiffres(n):
    """Renvoie le nombre de chiffres de l'entier positif n."""
    if n == 0:
        return 1
    compteur = 0
    while n > 0:
        n = n // 10
        compteur = compteur + 1
    return compteur

print(nombre_de_chiffres(2026))   # 4
print(nombre_de_chiffres(7))      # 1

# --- Exercice 5.1 ---
import math

def heron(a):
    """Calcule racine(a) par la methode de Heron."""
    x = float(a)
    while True:
        x_suivant = (x + a / x) / 2
        if abs(x_suivant - x) < 1e-15 * x:   # critère RELATIF
            return x_suivant
        x = x_suivant

print(heron(2))
print(math.sqrt(2))
print(abs(heron(2) - math.sqrt(2)))   # < 1e-12

# --- Exercice 6.1 ---
def vers_binaire(n):
    """Renvoie l'ecriture binaire de n sous forme de chaine, sans bin()."""
    if n == 0:
        return "0"
    resultat = ""
    while n > 0:
        resultat = str(n % 2) + resultat   # on met le chiffre DEVANT
        n = n // 2
    return resultat

print(vers_binaire(37))   # "100101"
print(vers_binaire(0))    # "0"
print(bin(37))            # "0b100101" -> verif

# Mon premier essai construisait "101001" au lieu de "100101", à l'envers. J'ai compris que % 2 donne le dernier chiffre, donc il faut l'ajouter au début de la chaîne, pas à la fin.
