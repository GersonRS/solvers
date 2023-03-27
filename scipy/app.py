import numpy as np

from scipy.optimize import linprog

# n = (float(input("Qual a recomendação de N? "))) / 1000
# p = (float(input("Qual a recomendação de P205? "))) / 1000
# k = (float(input("Qual a recomendação de K? "))) / 1000
n = 200 / 1000
p = 250 / 1000
k = 100 / 1000

c = np.array([2100, 1600, 1700, 2500, 1970, 1630, 1250, 2000, 1850])

Ac = np.array(
    [
        [0.45, 0.0, 0.0],
        [0.21, 0.0, 0.0],
        [0.32, 0.0, 0.0],
        [0.10, 0.52, 0.0],
        [0.16, 0.46, 0.0],
        [0.0, 0.44, 0.0],
        [0.0, 0.18, 0.0],
        [0.0, 0.0, 0.60],
        [0.20, 0.0, 0.20],
    ]
)

Ae = np.transpose(Ac)

be = np.array([n, p, k])

res = linprog(c, A_eq=Ae, b_eq=be, method="simplex")

# resultado = [{:8.2f}.format(res.x)]
# apresentando os resultados da otimização
print("Resultados obtidos com problemas de otimização de custos\n\n")
print(f"Custo total de adubação obtido (R$) = { np.format_float_positional(res.fun, precision=2) }")
print(f"Utilização de Uréia (kg) = { np.format_float_positional(res.x[0]*1000, precision=2) }")
print(f"Utilização de Sulfato de Amônia (kg) = {np.format_float_positional(res.x[1]*1000, precision=2)}")
print(f"Utilização de Nitrato de Amônia (kg) = {np.format_float_positional(res.x[2]*1000, precision=2)}")
print(f"Utilização de MAP (kg) = {np.format_float_positional(res.x[3]*1000, precision=2)}")
print(f"Utilização de DAP (kg) = {np.format_float_positional(res.x[4]*1000, precision=2)}")
print(f"Utilização de ST (kg) = {np.format_float_positional(res.x[5]*1000, precision=2)}")
print(f"Utilização de SS (kg) = {np.format_float_positional(res.x[6]*1000, precision=2)}")
print(f"Utilização de Kcl (kg) = {np.format_float_positional(res.x[7]*1000, precision=2)}")
print(f"Utilização de 20-00-20 (kg) = {np.format_float_positional(res.x[8]*1000, precision=2)}")
