import math

# --- 1. Calcul des notes de la gamme chromatique ---
# Le la 4 (A4) est à 440 Hz.
# La formule du tempérament égal : f(n) = 440 * 2^(n/12)
# où n est le nombre de demi-tons par rapport au La 4.

notes = []
frequencies = []
names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

print("=== Calcul des fréquences théoriques ===")
for n in range(-9, 3):  # On prend les 12 notes autour du La 4
    freq = 440 * (2 ** (n / 12))
    notes.append(n)
    frequencies.append(freq)
    name_idx = (n + 9) % 12
    print(f"Note {names[name_idx]} ({n:+2d} demi-tons) : {freq:.6f} Hz")

# --- 2. Construction d'un système linéaire simple ---
# On prend 3 notes pour "deviner" une note du milieu par interpolation linéaire.
# C'est ici qu'on utilise les notions de systèmes linéaires (même si c'est trivial).

# On choisit : Do (n=-9), Mi (n=-4), et on veut interpoler Ré (n=-7)
# Système : a * n^2 + b * n + c = freq  (on utilise un polynôme degré 2 pour plus de précision)
# Mais pour rester simple et montrer l'erreur flottante, on fait une interpolation linéaire simple :
# freq(x) = a * x + b

# On prend deux points : La4 (n=0, f=440) et Do5 (n=3, f=440*2^(3/12))
n1, f1 = 0, 440.0
n2, f2 = 3, 440 * (2 ** (3 / 12))

# Calcul des coefficients de la droite y = ax + b
a = (f2 - f1) / (n2 - n1)
b = f1 - a * n1

print("\n=== Interpolation linéaire ===")
print(f"Modèle fréquentiel simple : f(n) = {a:.4f} * n + {b:.4f}")

# On essaie de retrouver la fréquence du La4 par ce modèle
freq_calc_for_la = a * 0 + b
freq_true_for_la = 440.0

erreur_absolue = abs(freq_calc_for_la - freq_true_for_la)
erreur_relative = erreur_absolue / freq_true_for_la

print(f"\nFréquence vraie du La4 : {freq_true_for_la} Hz")
print(f"Fréquence calculée par interpolation : {freq_calc_for_la} Hz")
print(f"Erreur absolue : {erreur_absolue:.10e} Hz")
print(f"Erreur relative : {erreur_relative:.10e}")

# --- 3. Analyse de l'erreur de flottant sur la racine 12ème ---
print("\n=== Analyse de précision des flottants ===")
# On calcule 2^(1/12) plusieurs fois et on vérifie si le résultat est stable
val1 = 2 ** (1 / 12)
val2 = 2 ** (0.08333333333333333) # 1/12 en décimal approximatif
diff = abs(val1 - val2)
print(f"2^(1/12) via fraction exacte : {val1:.15f}")
print(f"2^(0.08333...) via décimal : {val2:.15f}")
print(f"Différence (instabilité flottante) : {diff:.15e}")

# --- 4. Conclusion personnelle ---
print("\n=== Réflexion ===")
if erreur_relative < 1e-10:
    print("L'erreur est négligeable pour l'oreille humaine, mais visible en précision machine.")
elif erreur_relative < 1e-5:
    print("L'erreur est faible, mais elle s'accumule si on itère le calcul.")
else:
    print("L'erreur est significative : le modèle linéaire est insuffisant pour la musique.")

print("Fin du projet.")
