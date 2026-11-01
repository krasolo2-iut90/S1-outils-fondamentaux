# ================================================================================
# TP5 - Chiffrer, dechiffrer, casser (chiffrement affine)
# ================================================================================


#===================================================================================
# Questionnaire
#===================================================================================

# Le chiffrement affine E(x) = (ax + b) mod 26 n'est reversible que si pgcd(a,26)=1
    # sinon deux lettres differentes peuvent donner la meme lettre chifffee
    # -> information detruite, aucun dechiffrement possible

# Il y a 312 cles valides : 12 valeurs de a x 26 valeurs de b

# Avec a = 1 on retrouve Cesar (simple decalage), avec a = 0 tout devient la lettre b

# La force brute suffit ici car 312 cles c'est minuscule pour un ordinateur
    # un chiffrement solide doit avoir un espace de clefs immense

# L'attaque par frequences marche car le chiffrement affine est une substitution :
    # la meme lettre du clair donne toujours la meme lettre du chiffe
    # donc les frequences du francais sont conservees, juste rebaptisees

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def euclide_etendu(a, b):
    if b == 0:
        return a, 1, 0
    g, u, v = euclide_etendu(b, a % b)
    return g, v, u - (a // b) * v
  
#====================================================================================
# Exercice 1.1 : les deux conversions
#====================================================================================

def lettre_vers_nombre(c):
    """Renvoie le rang de la majuscule c : A -> 0, B -> 1, ..., Z -> 25."""
    return ord(c) - ord("A")


def nombre_vers_lettre(n):
    """Renvoie la majuscule de rang n, modulo 26."""
    return chr(ord("A") + n % 26)


print(lettre_vers_nombre("C"))      # 2
print(nombre_vers_lettre(2))        # C
print(lettre_vers_nombre("A"), nombre_vers_lettre(0))
print(lettre_vers_nombre("Z"), nombre_vers_lettre(25))

# verif qu'elles sont bien reciproques sur tout l'alphabet
ok = all(nombre_vers_lettre(lettre_vers_nombre(chr(ord("A") + i))) == chr(ord("A") + i)
         for i in range(26))
print("reciproques sur A..Z :", ok)


# Note perso : j'ai d'abord ecrit `ord(c) - 65` au lieu de `ord("A")`.
# Ca marche mais c'est moins parlant, et je ne savais pas que 65 etait le code de A.


#====================================================================================
# Exercice 1.2 : nettoyer un texte
#====================================================================================

def nettoyer(texte):
    """Met en majuscules et ne garde que les lettres de A a Z."""
    return "".join(c for c in texte.upper() if "A" <= c <= "Z")


print(nettoyer("Été, à Paris !"))       # ETEAPARIS
print(nettoyer("Bonjour, le monde !"))  # BONJOURLEMONDE


# Note perso : premier essai avec `texte.upper()` puis test dans "ABCDEFGHIJKLMNOPQRSTUVWXYZ".
# Marchait aussi. Mais la comparaison "A" <= c <= "Z" est plus courte et elle exclut
# bien les caracteres accentues comme le E de ETES, qui restent hors de cet intervalle.


#====================================================================================
# Exercice 2.1 : chiffrer
#====================================================================================

def chiffrer(texte, a, b):
    """Applique E(x) = (a*x + b) mod 26 a chaque lettre d'un texte deja nettoye."""
    resultat = ""
    for c in texte:
        x = lettre_vers_nombre(c)
        resultat += nombre_vers_lettre((a * x + b) % 26)
    return resultat


print(chiffrer("ATTAQUEALAUBE", 5, 8))   # IZZIKECILIENC


#====================================================================================
# Exercice 3.1 : les cles utilisables
#====================================================================================

clefs_a = [a for a in range(1, 26) if pgcd(a, 26) == 1]
print(clefs_a)
print(len(clefs_a), "valeurs de a")


# Note perso : toutes impaires et sans le 13. Je m'attendais a ce que 13 passe
# (c'est impair), mais 13 = 26/2 donc pgcd(13,26) = 13. Et 26 = 2 * 13, donc
# tout multiple de 2 ou de 13 est exclu. Ca confirme que ce sont les facteurs
# de 26 qui comptent, pas la parite seule.


#====================================================================================
# Exercice 3.2 : l'inverse modulaire
#====================================================================================

def inverse_modulaire(a, n):
    """Renvoie a_inversible tel que a * a_inv = 1 (mod n), ou leve une erreur."""
    g, u, v = euclide_etendu(a, n)
    if g != 1:
        raise ValueError(f"{a} n'est pas inversible modulo {n} (pgcd = {g})")
    return u % n


print(inverse_modulaire(5, 26))          # 21
print(5 * 21, "=", 4 * 26 + 1)           # 105 = 105

for a in clefs_a:
    inv = inverse_modulaire(a, 26)
    assert (a * inv) % 26 == 1
print("verifie sur les 12 cles")


# Le `% n` a la fin est indispensable : euclide_etendu renvoie parfois un u negatif.
# Exemple : inverse_modulaire(3, 26) donne -8 sans le modulo, soit 18 avec.


#====================================================================================
# Le test demande dans "L'IA vous le donne en trois secondes"
#====================================================================================

def chiffrer_sans_test(texte, a, b):
    """Version naive, sans verification de la cle : celle qu'on trouve partout."""
    return "".join(nombre_vers_lettre((a * lettre_vers_nombre(c) + b) % 26) for c in texte)


clair = nettyoyer = nettoyer("LE CHIFFREMENT EST CASSE")
chiffre_4 = chiffrer_sans_test(clair, 4, 7)
print("avec a=4 :", chiffre_4)

# Combien de lettres distinctes dans le clair et dans le chiffe ?
print("lettres distinctes clair :", len(set(clair)))
print("lettres distinctes chiffre :", len(set(chiffre_4)))


# Conclusion de mon essai : a = 4 n'est pas dans la liste des 12 cles valides, et
# effectivement le message perd des informations. Deux lettres differentes du clair
# se retrouvent sur la meme lettre du chiffe, donc il est impossible de revenir en
# arriere. Le programme ne plante pas, il produit silencieusement un message
# irrecuperable. C'est exactement ce que l'enonce annoncait.


#====================================================================================
# Exercice 4.1 : dechiffrer
#====================================================================================

def dechiffrer(texte, a, b):
    """Dechiffre un texte affine. Refuse les cles invalides."""
    a_inv = inverse_modulaire(a, 26)     # leve ValueError si a non inversible
    return "".join(nombre_vers_lettre(a_inv * (lettre_vers_nombre(c) - b))
                   for c in texte)


m = nettoyer("L'attaque aura lieu a l'aube")
print(dechiffrer(chiffrer(m, 5, 8), 5, 8) == m)     # True

try:
    dechiffrer("ABC", 4, 7)
except ValueError as e:
    print("cle refusee :", e)


# Note perso : j'ai oublie le `% 26` dans un premier temps alors que `lettre_vers_nombre(c) - b`
# peut devenir negatif. Python gere bien les restes negatifs (-3 % 26 = 23), donc
# nombre_vers_lettre avec son propre modulo rattrape le coup, mais je prefere le savoir.


#====================================================================================
# Exercice 5.1 : attaque par force brute
#====================================================================================

def toutes_les_clefs(secret):
    """Renvoie la liste des (a, b, texte_dechiffre) pour toutes les cles valides."""
    propositions = []
    for a in clefs_a:
        for b in range(26):
            propositions.append((a, b, dechiffrer(secret, a, b)))
    return propositions


secret = nettoyer("IZZIKECILIENC")
propositions = toutes_les_clefs(secret)
print(len(propositions), "propositions testees")

for a, b, texte in propositions:
    if "A" in texte and "E" in texte and "U" in texte:
        print(f"a={a:>2} b={b:>2} : {texte}")


# Note perso : j'ai filtre grossierement sur la presence de A, E, U pour ne pas lire
# les 312 lignes. Ca laisse encore quelques candidats, mais un seul est du francais
# reel. C'est la limite de la force brute : le calcul est gratuit, le tri ne l'est pas.


#====================================================================================
# Exercice 6.1 : attaque par analyse de frequences
#====================================================================================

frequences_francais = {
    "E": 0.150, "A": 0.076, "S": 0.075, "N": 0.070, "I": 0.073,
    "T": 0.065, "R": 0.063, "L": 0.055, "U": 0.049, "O": 0.054,
    "D": 0.035, "C": 0.030, "P": 0.025, "M": 0.025, "G": 0.010,
    "B": 0.010, "V": 0.008, "F": 0.010, "H": 0.008, "J": 0.002,
    "K": 0.005, "Q": 0.002, "W": 0.003, "X": 0.003, "Y": 0.003, "Z": 0.005,
}


def compter(texte):
    """Nombre d'occurrences de chaque lettre du texte."""
    compte = {c: 0 for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for c in texte:
        compte[c] += 1
    return compte


def lettre_la_plus_frequente(texte):
    compte = compter(texte)
    return max(compte, key=lambda c: compte[c])


def candidates_par_frequence(secret):
    """Teste seulement les cles qui envoient E sur la lettre la plus frequente."""
    cible = lettre_la_plus_frequente(secret)
    rang_cible = lettre_vers_nombre(cible)
    candidats = []
    for a in clefs_a:
        a_inv = inverse_modulaire(a, 26)
        # on veut E (rang 4) envoye sur cible : a*4 + b = rang_cible (mod 26)
        b = (rang_cible - a * 4) % 26
        candidats.append((a, b, dechiffrer(secret, a, b)))
    return cible, candidats


cible, candidats = candidates_par_frequence(secret)
print("lettre la plus frequente du secret :", cible)
print(len(candidats), "candidats au lieu de 312")
for a, b, texte in candidats:
    print(f"a={a:>2} b={b:>2} : {texte}")


# Note perso : ca ramene 312 hypotheses a 12, et parmi elles une seule se lit.
# Par contre j'ai du garder l'oeil humain pour choisir. Pour supprimer totalement
# l'intervention humaine il faudrait noter chaque candidat (produit des frequences
# observees par les frequences attendues), ce que je n'ai pas fait ici.


#====================================================================================
# Comparaison des deux attaques
#====================================================================================

print(f"force brute : {len(propositions)} dechiffrements a calculer et a regarder")
print(f"analyse de frequences : {len(candidats)} dechiffrements a calculer")
