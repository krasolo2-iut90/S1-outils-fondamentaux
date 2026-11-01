# TP - Solutions

J'ai regroupé mes commentaires sur les tp dans ce fichier.

## TP1 - Calcul numérique

Arrêté à l'exercice 6.2 (étape 7 non faite).

### Ce que je retiens

- `10 / 5` vaut `2.0` et non `2` : c'est l'erreur que j'ai faite le plus souvent,
  notamment à l'exercice 3.2 et dans `vers_binaire`.
- Deux flottants ne se comparent jamais avec `==`. Mon test `0.1 + 0.2 == 0.3`
  renvoyait `False` et je pensais que c'était Python qui bugait.
- L'exercice 6.1 m'a posé problème : j'inversais l'ordre des chiffres binaires.
  En fait `% 2` donne le **dernier** chiffre, il faut donc l'ajouter au début de
  la chaîne et non à la fin.
- Le critère d'arrêt de Heron avec un seuil absolu (`1e-15`) marche bien pour
  `heron(2)`, mais devient trop strict dès que `a` est très grand : l'écart entre
  deux estimations y est naturellement supérieur à ce seuil. Il faudrait un
  critère relatif.

## TP2 - Arithmétique et nombres premiers

Tous les exercices sont faits, y compris les prolongements (nombre de tours de
Heron, module decimal).

### Ce que je retiens

- **Euclide étendu (ex7.1)** : c'est l'exercice qui m'a le plus bloqué. La
  récurrence `g, v, u - (a//b)*v` est contre-intuitive. J'ai vérifié à la main
  sur 1071 et 462 : u = -3, v = 7, et `-3*1071 + 7*462 = 21`. Ça marche, mais il
  a fallu que je trace le calcul pas à pas sur papier pour y croire.
- **Fibonacci exponentiel (ex6.2)** : F(30) rappelle F(1) 832 040 fois, pour
  près de 2,7 millions d'appels au total. L'algorithme itératif (ex6.3) fait le
  même calcul en 30 tours. C'est la différence concrète entre O(2^n) et O(n),
  et je ne l'avais jamais vraiment ressenti avant de compter les appels.
- **Crible vs test un par un (ex4)** : la crible gagne largement pour compter
  tous les premiers sous 100 000 (9592 des deux côtés, bon contrôle croisé).
  Mais si on ne teste qu'un seul nombre, le test à la racine carrée est déjà
  très efficace et la crible perd son intérêt.
- **Puissance modulaire rapide (ex7.2)** : au lieu de `e` multiplications, on
  fait un nombre d'itérations égal au nombre de bits de `e`. Pour e = 10^7
  (~24 bits), c'est une vingtaine de tours au lieu de dix millions.
- **La dernière ligne de `facteurs`** : j'ai d'abord oublié le `if n > 1`, et
  du coup je perdais le facteur premier plus grand que la racine carrée. Le test
  "le produit des facteurs doit redonner n" m'a permis de le voir.

## TP3 - Polynômes et fonctions

Tous les exercices sont faits, y compris l'étape 5 (traces matplotlib).

### Résultats mesurés

- **Horner vs naïve (ex2)** : à `x = 1.0001`, le rapport de vitesse reste vers 2
  quand le degré passe de 1000 à 20000. À `x = 3` (entier), le rapport monte de
  4 à 6 avec le degré. Ce n'était pas ma prévision : j'attendais un gain
  quadratique. La raison est que `x ** i` en Python est un appel de fonction
  déjà assez coûteux, mais pas `i` fois pire qu'une multiplication.
- **Newton (ex4)** : sur x^3 - 2x - 5, cinq tours depuis 2 mais une vingtaine
  depuis 0. Sur x^3 - 2x + 2 en partant de 0, ça ne converge pas du tout : le
  trajet oscille entre 0 et 1 indéfiniment. Le trace des itérés rend le
  phénomène immédiat à comprendre, beaucoup plus que le tableau de nombres.
- **Triangle de Pascal (ex6.2)** : en multipliant dix fois [1,1] par lui-même
  on retrouve bien `[1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]`, et la
  somme des coefficients vaut bien 2^10.
- **Le mur des flottants (ex7)** : l'erreur diminue puis remonte. Meilleur pas
  vers 1e-8 pour la formule avant, 1e-6 pour la centrée. À h = 1e-12 l'erreur a
  remonté de plusieurs ordres de grandeur.
- **Intégration (ex8)** : Simpson donne x^2 exactement (erreur ~1e-17, soit le
  bruit de la machine). Pour pi, trapèzes erreur ~1e-7, Simpson indiscernable de
  math.pi.

### Ce que je n'avais pas compris au départ

Je pensais que diminuer `h` améliorait toujours la dérivée numérique. En fait
`f(x+h) - f(x)` soustrait deux nombres presque égaux : c'est exactement
l'élimination catastrophique du TP1, retrouvée ici par un autre chemin. Les deux
TP se rejoignent sans que ce soit évident sur le moment.

## TP4 - Matrices et systèmes linéaires

Tous les exercices sont faits, y compris les étapes 7 et 8.

### Résultats mesurés

- **Produit matriciel (ex2)** : le temps est bien multiplié par environ 8 quand
  la taille double, ce qui confirme le coût en n^3.
- **Python pur vs numpy (ex3)** : pour n = 120, numpy est environ 1000 fois plus
  rapide. Le facteur est bien plus brutal que ce que j'imaginais.
- **Pivot de Gauss (ex4)** : ma solution coincide avec `np.linalg.solve` à moins
  de 1e-9 près sur un système aléatoire de taille 50. Le pivot partiel n'est pas
  décoratif : sans lui, diviser par un pivot minuscule amplifie l'erreur.
- **Matrice de Hilbert (ex5)** : conditionnement de l'ordre de 1e14. Avec
  `inv(H) @ b` l'erreur dépasse 0.5, alors que `solve(H, b)` s'en sort mieux mais
  reste faux. Les deux sont inutilisables : quand le conditionnement explose,
  aucun algorithme en flottants ne sauve le problème.
- **Hilbert vaincue (ex8.1)** : premier essai en `Fraction` -> "système
  singulier". La cause n'était pas la matrice mais mon propre seuil `1e-14` :
  certains pivots rationnels sont réels mais minuscules, et mon test les
  déclarait nuls. En passant `tolerance=0`, j'obtiens exactement douze fois
  `Fraction(1, 1)`, là où `solve` se trompait de plus de 0.5.

### Ce qui m'a plu

L'exercice 8.1 est celui que je retiens : le même code, sans une seule ligne
changée, résout exactement ce qui échouait complètement trente lignes plus haut.
Le seul changement est le type des nombres. Ça rend concret quelque chose qui
restait abstrait depuis le TP1.

## Usage d'un assistant

Autorisé et utilisé. Je m'en suis servi pour écrire une partie du code, relire
mes erreurs de syntaxe et comprendre certaines récursions (notamment Euclide
étendu). J'ai exécuté chaque exercice moi-même et vérifié les résultats annoncés.
Les commentaires de réflexion ci-dessus sont les miens.
