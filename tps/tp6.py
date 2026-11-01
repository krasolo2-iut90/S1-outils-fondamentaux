import math
import random


# ================================================================================
# TP6 - Géométrie du plan
# ================================================================================


#===================================================================================
# Questionnaire
#===================================================================================

# Le produit scalaire donne l'angle entre deux vecteurs via cos(theta) = (u.v) / (|u|*|v|)
    # si le produit scalaire est nul, les vecteurs sont perpendiculaires

# Le determinant u_x * v_y - u_y * v_x est une aire orientee
    # positif si u->v tourne dans le sens trigonometrique (gauche)
    # negatif si ca tourne a droite
    # nul si alignes

# L'aire d'un polygone avec la formule du lacet (shoelace formula)
    # somme des determinants des cotes consecutifs, divisee par 2
    # marche pour les polygones simples (non croises)

# Le lancer de rayon (ray casting) pour savoir si un point est dans un polygone
    # on compte les intersections avec un rayon horizontal partant du point
    # impair = dedans, pair = dehors
    # les cas limites (point sur un sommet ou un cote) sont delicats


#====================================================================================
# Exercice 1.1 : la boite a outils
#====================================================================================

def vecteur(A, B):
    """Vecteur AB = B - A."""
    return (B[0] - A[0], B[1] - A[1])


def produit_scalaire(u, v):
    """Produit scalaire de u et v."""
    return u[0] * v[0] + u[1] * v[1]


def norme(u):
    """Norme (longueur) du vecteur u."""
    return math.sqrt(produit_scalaire(u, u))


def angle(u, v):
    """Angle en degres entre les vecteurs u et v."""
    cos_theta = produit_scalaire(u, v) / (norme(u) * norme(v))
    # borne dans [-1, 1] pour eviter les erreurs flottantes
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.degrees(math.acos(cos_theta))


print(norme((3, 4)))            # 5.0
print(produit_scalaire((1, 2), (3, 4)))  # 11
print(angle((1, 0), (1, 1)))    # 45.0
print(angle((1, 0), (0, 1)))    # 90.0


# Note perso : j'ai oublie le `math.sqrt` dans `norme` au debut, donc j'avais la
# norme au carre. Et j'ai du faire le `max(-1, min(1, cos_theta))` car
# `norme((1,0)) * norme((1,1))` peut donner `1.0000000000000002` a cause des
# flottants, et `acos(1.000...02)` plante avec un domaine error.


#====================================================================================
# Exercice 1.2 : distance d'un point a une droite
#====================================================================================

def determinant(u, v):
    """Determinant u_x * v_y - u_y * v_x (aire orientee)."
    """
    return u[0] * v[1] - u[1] * v[0]


def distance_point_droite(P, A, B):
    """Distance du point P a la droite (AB)."""
    ab = vecteur(A, B)
    ap = vecteur(A, P)
    return abs(determinant(ab, ap)) / norme(ab)


# distance de l'origine a la droite (0,1)-(1,0)
print(distance_point_droite((0, 0), (0, 1), (1, 0)))  # 0.7071... = sqrt(2)/2
# distance de (3,4) a l'axe des abscisses (y=0)
print(distance_point_droite((3, 4), (0, 0), (1, 0)))  # 4.0


#====================================================================================
# Exercice 2.1 : a gauche ou a droite ?
#====================================================================================

def orientation(A, B, C):
    """Retourne 1 si A->B->C tourne a gauche, -1 a droite, 0 si aligne."""
    ab = vecteur(A, B)
    ac = vecteur(A, C)
    det = determinant(ab, ac)
    if det > 0:
        return 1
    elif det < 0:
        return -1
    else:
        return 0


print(orientation((0, 0), (1, 0), (1, 1)))   # 1 (gauche)
print(orientation((0, 0), (1, 0), (1, -1)))  # -1 (droite)
print(orientation((0, 0), (1, 1), (2, 2)))   # 0 (aligne)


# Note perso : j'avais commence par comparer `det == 0` pour l'alignement.
# C'est une faute en calcul flottant. Il faut comparer a une tolerance, mais ici
# les tests utilises ont des coordonnees entieres, donc le determinant est entier
# et `== 0` marche. Pour des coords flottantes, il faudrait `abs(det) < epsilon`.


#====================================================================================
# Exercice 2.2 : l'aire d'un polygone
#====================================================================================

def aire(polygone):
    """Aire du polygone par la formule du lacet (shoelace)."""
    n = len(polygone)
    s = 0.0
    for i in range(n):
        j = (i + 1) % n
        s += determinant(polygone[i], polygone[j])
    return abs(s) / 2.0


# carre unite
print(aire([(0, 0), (1, 0), (1, 1), (0, 1)]))       # 1.0
# triangle (0,0)-(4,0)-(0,3)
print(aire([(0, 0), (4, 0), (0, 3)]))                 # 6.0
# maison du TP4
maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
print(aire(maison))                                    # 4.0


#====================================================================================
# Exercice 3.1 : le test de croisement
#====================================================================================

def se_coupent(A, B, C, D):
    """Renvoie True si les segments [AB] et [CD] se coupent strictement.
    
    Ne traite pas les cas ou trois points sont alignes (renvoie False).
    """
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    
    # si trois points alignes, on renvoie False (cas non traite)
    if o1 == 0 or o2 == 0 or o3 == 0 or o4 == 0:
        return False
    
    # C et D de part et d'autre de (AB), et A et B de part et d'autre de (CD)
    return (o1 != o2) and (o3 != o4)


# diagonales du carre unite : (0,0)-(1,1) et (1,0)-(0,1)
print(se_coupent((0, 0), (1, 1), (1, 0), (0, 1)))  # True
# segments paralleles
print(se_coupent((0, 0), (1, 0), (0, 1), (1, 1)))   # False
# segments alignes mais disjoints
print(se_coupent((0, 0), (1, 1), (2, 2), (3, 3)))   # False


#====================================================================================
# Exercice 3.2 : le point d'intersection
#====================================================================================

def intersection(A, B, C, D):
    """Renvoie le point d'intersection des segments [AB] et [CD], ou None."""
    if not se_coupent(A, B, C, D):
        return None
    
    # t = det(AC, CD) / det(AB, CD)
    # u = det(AC, AB) / det(AB, CD)
    ab = vecteur(A, B)
    ac = vecteur(A, C)
    cd = vecteur(C, D)
    
    denom = determinant(ab, cd)
    if denom == 0:
        return None  # paralleles, ne devraient pas arriver ici
    
    t = determinant(ac, cd) / denom
    x = A[0] + t * ab[0]
    y = A[1] + t * ab[1]
    return (x, y)


# diagonales du carre de cote 2 : (0,0)-(2,2) et (2,0)-(0,2)
print(intersection((0, 0), (2, 2), (2, 0), (0, 2)))  # (1.0, 1.0)


#====================================================================================
# Exercice 4.1 : le lancer de rayon
#====================================================================================

def dedans(P, polygone):
    """Renvoie True si le point P est strictement a l'interieur du polygone.
    
    Algorithme du lancer de rayon horizontal vers la droite.
    Les cas limites (sur un cote ou un sommet) ne sont pas traites specialement.
    """
    n = len(polygone)
    compteur = 0
    px, py = P
    
    for i in range(n):
        Si = polygone[i]
        Sj = polygone[(i + 1) % n]
        si_x, si_y = Si
        sj_x, sj_y = Sj
        
        # le rayon traverse le cote si les ordonnees encadrent py
        # et strictement : on exclut le sommet le plus haut pour eviter le double comptage
        if (si_y > py) != (sj_y > py):
            # abscisse du point de croisement par interpolation
            x_intersect = si_x + (py - si_y) / (sj_y - si_y) * (sj_x - si_x)
            if x_intersect > px:
                compteur += 1
    
    return compteur % 2 == 1


# verification sur la maison
print("dedans (1,1):", dedans((1, 1), maison))       # True
print("dedans (1, 2.4):", dedans((1, 2.4), maison))  # True
print("dedans (3,1):", dedans((3, 1), maison))       # False
print("dedans (0.2, 2.2):", dedans((0.2, 2.2), maison))  # False


# Note perso : la condition `(si_y > py) != (sj_y > py)` est astucieuse : elle
# exclut le sommet dont l'ordonnee est la plus grande, evitant ainsi de compter
# deux fois un sommet quand le rayon passe dessus. C'est la convention standard
# pour le lancer de rayon.


#====================================================================================
# Exercice 4.2 : l'aire par Monte-Carlo
#====================================================================================

def aire_monte_carlo(polygone, nb_points=200000, seed=42):
    """Estime l'aire du polygone par la methode de Monte-Carlo."""
    random.seed(seed)
    
    # trouver le rectangle englobant
    xs = [p[0] for p in polygone]
    ys = [p[1] for p in polygone]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    aire_rect = (x_max - x_min) * (y_max - y_min)
    
    dedans_count = 0
    for _ in range(nb_points):
        px = random.uniform(x_min, x_max)
        py = random.uniform(y_min, y_max)
        if dedans((px, py), polygone):
            dedans_count += 1
    
    return dedans_count / nb_points * aire_rect


print(aire_monte_carlo(maison, 200000, 42))  # ~4.0


#====================================================================================
# Exercice 5.1 : un polygone non convexe (en forme de L)
#====================================================================================

polygone_L = [(0, 0), (0, 2), (1, 2), (1, 1), (2, 1), (2, 0)]

print("aire L:", aire(polygone_L))   # 3.0 (deux carres de cote 1 + un carre de cote 1 = 3)
print("dedans (0.5, 0.5):", dedans((0.5, 0.5), polygone_L))  # True
print("dedans (1.5, 0.5):", dedans((1.5, 0.5), polygone_L))  # True
print("dedans (0.5, 1.5):", dedans((0.5, 1.5), polygone_L))  # True
print("dedans (1.5, 1.5):", dedans((1.5, 1.5), polygone_L))  # False (dans le creux)


# Note perso : le creux du L est bien detecte comme "dehors". C'est important car
# un polygone non convexe a des parties "vides" que le lancer de rayon detecte
# correctement (le rayon traverse un cote pour entrer, et un autre pour sortir dans
# le creux, donc compteur pair = dehors).


#====================================================================================
# Exercice 6.1 : le polygone le plus proche
#====================================================================================

def zone_de(P, zones):
    """Renvoie l'indice de la zone contenant P, ou None."""
    for i, zone in enumerate(zones):
        if dedans(P, zone):
            return i
    return None


zone_maison = maison
zone_carre = [(3, 0), (4, 0), (4, 1), (3, 1)]
zones = [zone_maison, zone_carre]

print(zone_de((1, 1), zones))        # 0 (dans la maison)
print(zone_de((3.5, 0.5), zones))    # 1 (dans le carre)
print(zone_de((2.5, 0.5), zones))    # None (dans aucune)


# Note perso : cette fonction est naive : elle parcourt toutes les zones dans
# l'ordre. Pour beaucoup de zones, il faudrait une structure de donnees plus
# efficace (quadtrees, grille spatiale). Mais pour quelques zones, ca suffit.
