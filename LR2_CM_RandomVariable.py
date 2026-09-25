import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from math import *
from random import *

l = 1
n = 100
a = []

for j in range(n):
    u = uniform(0, 1)
    i = 0
    p = exp(-l)
    f = p
    while u >= f:
        p = l * p / (i + 1)
        f = f + p
        i += 1
    x = i
    a.append(x)

v = [a.count(x) for x in sorted(set(a))]
print("x_i ", sorted(set(a)))
print("n_i ", v)

s = 0
for i in range(len(set(a))):
    s += sorted(set(a))[i] * v[i]
x_ = s / n
l_z = x_
print(f"x_ = {x_}, l_z = {l_z}")

p = []
for i in range(len(set(a))):
    p.append(exp(-l_z) * (l_z**i / factorial(i)))
print("p = ", p)

tab = [list() for i in range(len(set(a)))]
for i in range(len(set(a))):
    tab[i].append(i + 1)
    tab[i].append(v[i])
    tab[i].append(n * p[i])
    tab[i].append(tab[i][1] - tab[i][2])
    tab[i].append((tab[i][1] - tab[i][2])**2)
    tab[i].append(tab[i][4] / tab[i][2])

print("\n" + "="*100)
print("ТАБЛИЦА tab")
print("="*100)
headers = ["i", "n_i", "n_i'", "n_i-n_i'", "(n_i-n_i')^2", "xi^2"]
print("  ".join(f"{h:^15}" for h in headers))
print("-"*100)
for row in tab:
    print(f"{row[0]:^15} {row[1]:^15} {row[2]:^15.2f} "
          f"{row[3]:^15.2f} {row[4]:^15.2f} {row[5]:^15.3f}")

xi = sum(tab[i][-1] for i in range(len(set(a))))
xi_tab = 11.1 #0.05
print(f"xi = {xi}, xi_tab = {xi_tab}")

if xi < xi_tab:
    print("wow")
else:
    print("cringe")











plt.figure(figsize=(10, 6))
sns.histplot(a, bins=range(min(a), max(a) + 2), kde=False,
            color='skyblue', edgecolor='black', alpha=0.7)
plt.title("Гистограмма частот (распределение Пуассона, λ = 2)", fontsize=14)
plt.xlabel("Значение X", fontsize=12)
plt.ylabel("Частота", fontsize=12)
plt.xticks(range(min(a), max(a) + 1))
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

