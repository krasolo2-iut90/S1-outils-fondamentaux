import math

print("=== 1. Calcul des fréquences théoriques ===")
names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
# On calcule tout le spectre autour du La 4
freqs = {}
for n in range(-9, 3):
    freqs[n] = 440 * (2 ** (n / 12))
    name_idx = (n + 9) % 12
    print(f"Note {names[name_idx]:<2} ({n:+2d}) : {freqs[n]:.6f} Hz")

# --- 2. Interpolation : Tester un point INTERMÉDIAIRE ---
# On prend deux bornes éloignées : Do (-9) et Si (+2)
n1, f1 = -9, freqs[-9]
n2, f2 = 2, freqs[2]

# On construit la droite entre ces deux notes
a = (f2 - f1) / (n2 - n1)
b = f1 - a * n1

print("\n=== 2. Test d'interpolation linéaire (Modèle simpliste) ===")
print(f"Modèle : f(n) = {a:.4f} * n + {b:.4f}")

# On teste au milieu : le La4 (n=0), qui n'est PAS une borne !
n_test = 0
f_theorique = freqs[n_test]
f_interpolee = a * n_test + b

erreur_abs = abs(f_theorique - f_interpolee)
erreur_rel = erreur_abs / f_theorique

print(f"Vraie fréquence du La4 : {f_theorique:.6f} Hz")
print(f"Fréquence interpolée   : {f_interpolee:.6f} Hz")
print(f"Erreur absolue         : {erreur_abs:.6f} Hz")
print(f"Erreur relative        : {erreur_rel:.4%}")

# --- 3. Précision Flottante : L'accumulation d'erreurs ---
# Au lieu de comparer 1/12 et 0.0833..., on va accumuler l'erreur.
# On part du La4 et on monte de 12 demi-tons en multipliant par le ratio flottant.
# Théoriquement, on doit retomber pile sur 880 Hz (une octave au-dessus).

print("\n=== 3. Accumulation d'erreurs flottantes (Le test de l'octave) ===")
ratio = 2 ** (1/12)
freq_actuelle = 440.0

for i in range(12):
    freq_actuelle *= ratio

freq_theorique_octave = 440.0 * 2 # Une octave au-dessus = x2

print(f"Résultat après 12 multiplications flottantes : {freq_actuelle:.15f}")
print(f"Valeur théorique exacte                      : {freq_theorique_octave:.15f}")
print(f"Différence (Erreur machine)                  : {abs(freq_actuelle - freq_theorique_octave):.15e}")

if abs(freq_actuelle - freq_theorique_octave) > 0:
    print(">>> CONCLUSION : Les flottants ne sont pas exacts. L'erreur s'accumule.")
else:
    print(">>> CONCLUSION : Hasard chanceux, réessaie avec plus d'octaves.")
