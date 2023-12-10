import qsharp
import math
import matplotlib.pyplot as plt
from PhaseEstimation import run

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

### ALGO.Q ###

n_shots = 14
n_oracle = 3
phi = 0

theta = (2 / n_oracle) * (math.pi / 4)

result = run.simulate(nShots=n_shots, phi=phi, oraclePower=n_oracle)

print(result)

### FUNCTION ###


def res_nshot(n, phi, n_oracle):
    n_values = list(range(1 ,n))
    results_nshot = [run.simulate(nShots=n, phi=phi, oraclePower=n_oracle) for n in n_values]
    new_results_nshot = []
    for (a,b) in results_nshot:
        p_esti = b / (a + b)
        phi_esti = (2/n_oracle) * (math.asin(math.sqrt(p_esti)) - (math.pi / 4))
        new_results_nshot.append(abs(phi_esti - phi))
    return new_results_nshot

def res_noracle(n, phi, n_shots):
    n_values = list(range(1 ,n))
    results_noracle = [run.simulate(nShots=n_shots, phi=phi, oraclePower=n) for n in n_values]
    new_results_noracle = []
    i = 1
    for (a,b) in results_noracle:
        p_esti = b / (a + b)
        phi_esti = (2/i) * (math.asin(math.sqrt(p_esti)) - (math.pi / 4))
        new_results_noracle.append(abs(phi_esti - phi))
        i += 1
    return new_results_noracle

### COURBE ###

n = 100
phi = 0
n_shots = 50
n_oracle = 50

new_results_nshot = res_noracle(n, phi, n_oracle)
new_results_noracle = res_nshot(n, phi, n_shots)
n_values = list(range(1 ,n))

### TEST FIT FOR N_SHOT ###

# Vos données
x_data = np.array(n_values)  # Assurez-vous que x_data ne contient pas de zéro
y_data = np.array(new_results_nshot)  # ou new_results_nshot
y_data2 = np.array(new_results_noracle)  # ou new_results_noracle

# Fonction modèle a / x^b
def power_inverse_model(x, a, b):
    return a / np.power(x, b)

# Vérifiez que x_data ne contient pas de zéro pour éviter une division par zéro
if 0 in x_data:
    raise ValueError("x_data ne doit pas contenir de zéro.")

# Effectuez l'ajustement de courbe
params, covariance = curve_fit(power_inverse_model, x_data, y_data)
params2, covariance2 = curve_fit(power_inverse_model, x_data, y_data2)


# Obtenez les paramètres ajustés
a, b = params
a2, b2 = params2

print("A / X^B")

print("N SHOT")
print("A : " + str(a))
print("B : " + str(b))

print("N ORACLE")
print("A : " + str(a2))
print("B : " + str(b2))

# Tracez les données et la courbe ajustée
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = power_inverse_model(x_fit, a, b)
y_fit2 = power_inverse_model(x_fit, a2, b2)

plt.scatter(x_data, y_data, label='Données - variation n_shot')
plt.plot(x_fit, y_fit, label='Courbe ajustée (' + str(a) + ' / x^' + str(b) + ')', color='blue')
plt.scatter(x_data, y_data2, label='Données - variation n_oracle')
plt.plot(x_fit, y_fit2, label='Courbe ajustée (' + str(a2) + ' / x^' + str(b2) + ')', color='red')

plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.show()

### CONCLUSION ###

## On observe que la courbe tant plus vers 0 en augmentant le nombre d'oracle que en augmentant le nombre de shots
## Cependant, il faut préciser qu'il faut un minimum de nombre de shots avant d'augmenter le nombre d'oracle