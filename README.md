# Projet : Accord chromatique et limites des flottants

## Contexte personnel
Je m'appelle Kenza Rasolo, du groupe C1. J'aime la musique, ce projet en est donc né par une question toute simple en accordant un instrument : pourquoi les fréquences des notes ne tombent-elles jamais "pile" ? La réponse est à moitié musicale, à moitié numérique, et c'est cette seconde moitié qui m'intéressait.

## Question de départ
Peut-on retrouver les fréquences de la gamme chromatique avec un modèle simple (interpolation linéaire), et jusqu'où la précision flottante nous laisse-t-elle tomber ?

## Démarche
1. Calcul des 12 fréquences du tempérament égal à partir du La 4 = 440 Hz, via f(n) = 440 * 2^(n/12).
2. Interpolation linéaire entre deux notes extrêmes (Do et Si), puis test au milieu de l'intervalle, là où le modèle n'a pas été calibré.
3. Test d'accumulation : monter d'une octave en multipliant 12 fois de suite par 2^(1/12), et comparer au résultat théorique (exactement 880 Hz).

Tout est écrit en Python brut, sans NumPy, pour garder la main sur chaque opération et voir exactement ce que la machine calcule.

## Résultats mesurés

### L'interpolation linéaire échoue
Modèle calibré sur Do (-9) et Si (+2) : f(n) = 21.1143*n + 451.6546

| | Valeur |
|---|---|
| Fréquence vraie du La4 | 440.000000 Hz |
| Fréquence interpolée | 451.654622 Hz |
| Erreur absolue | 11.654622 Hz |
| Erreur relative | 2.65 % |

### Les flottants accumulent une erreur réelle
Après 12 multiplications successives par 2^(1/12) en partant de 440 Hz :

- Résultat calculé : 880.000000000000341
- Valeur théorique : 880.000000000000000
- Écart : 3.410605131648481e-13 Hz

## Analyse

**Pourquoi l'erreur de 11.65 Hz était prévisible.** La gamme n'est pas linéaire mais exponentielle: chaque note s'obtient en *multipliant* par un ratio constant, pas en ajoutant une constante. Remplacer une exponentielle par une droite donne forcément une erreur maximale au milieu de l'intervalle, loin des points de calibration. C'est exactement ce que j'ai observé.

**Ce que ça change concrètement.** En musique, un demi-ton vaut environ 26 Hz autour de 440 Hz. Mon erreur de 11.65 Hz représente donc près d'un *quart de demi-ton*. L'oreille entraînée perçoit un écart bien plus petit que ça. Autrement dit : mon modèle numérique produirait un instrument faux, audiblement. Le flottant n'est pas le problème ici, c'est le modèle.

**Et l'erreur de 3.41e-13 ?** Elle est mille milliards de fois trop petite pour l'oreille humaine. Mais elle existe, et surtout elle *s'accumule* : à chaque multiplication, l'arrondi se propage. Sur une octave, c'est invisible. Dans un logiciel de synthèse sonore qui empile des milliers d'opérations, ou dans une simulation scientifique itérative, ce n'est plus négligeable. C'est le même phénomène qu'en chimie quand on propager des incertitudes de mesure le long d'un calcul.

## Limites identifiées
- Je n'ai testé qu'un seul point d'interpolation. Une étude complète tracerait l'erreur sur tout l'intervalle, ce qui dessinerait une courbe en cloche.
- Je compare avec la valeur théorique du tempérament égal, mais les instruments réels (piano accordé à l'oreille, cordes frottées) s'en écartent volontairement.
- Le test d'octave dépend de la chance : selon les valeurs, l'erreur peut sembler s'annuler. Un test sur 100 octaves serait plus parlant.

## Usage d'un assistant
J'ai utilisé un assistant IA pour écrire une partie du code et corriger des erreurs de syntaxe. J'ai vérifié moi-même chaque résultat affiché, j'ai relu les formules musicales, et j'ai rédigé seul l'analyse ci-dessus.

## Fichiers
- `main.py` : le programme
- `results.txt` : la sortie brute du programme
