import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from math import *
from random import *

l = 0.1
n = 100
a = []

for i in range(n):
    u = random()
    x = - (1 / l) * log(1 - u)
    a.append(x)

k = floor(1 + log2(n))
x_max = max(a)
x_min = min(a)
lenght = ceil((x_max - x_min) / k)

print(f"x_min = {x_min}, x_max = {x_max}, k = {k}, lenght = {lenght}")
interval = [list() for i in range(k)]
prev = 0
for i in range(k):
    interval[i].append(prev)
    interval[i].append(prev + lenght)
    interval[i].append((prev + prev + lenght) / 2)
    interval[i].append( len([x for x in a if prev <= x <= prev + lenght]) )
    prev = prev + lenght

x_b = sum(s[2] * s[3] for s in interval) / n
l_z = 1 / x_b
print(f"x_b = {x_b}, l_z = {l_z}")

for i in range(k):
    interval[i].append( exp(-l_z * interval[i][0]) - exp(-l_z * interval[i][1]) )
    interval[i].append( n * interval[i][4])

print("\n" + "="*80)
print("ТАБЛИЦА interval")
print("="*80)
headers = ["Интервал", "(x_i + x_i-1) / 2", "n_i", "p_i", "n_i'"]
print("  ".join(f"{h:^15}" for h in headers))
print("-"*80)
for row in interval:
    interval_str = f"{row[0]:.2f} – {row[1]:.2f}"
    print(f"{interval_str:^15} "
          f"{row[2]:^15.2f} "
          f"{row[3]:^15} "
          f"{row[4]:^15.4f} "
          f"{row[5]:^15.2f}")

tab = [list() for i in range(k)]
for i in range(k):
    tab[i].append(i + 1)
    tab[i].append(interval[i][3])
    tab[i].append(interval[i][5])
    tab[i].append(interval[i][3] - interval[i][5])
    tab[i].append((interval[i][3] - interval[i][5])**2)
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

xi = sum(tab[i][-1] for i in range(k))
xi_tab = 11.1 #0.05
print(f"xi = {xi}, xi_tab = {xi_tab}")

if xi < xi_tab:
    print("wow")
else:
    print("cringe")

plt.subplot(1, 2, 1)
sns.histplot(a, bins=k, kde=False, color='skyblue', edgecolor='black')
plt.title("Гистограмма частот")
plt.xlabel("Значение X")
plt.ylabel("Частота")
plt.grid(axis='y', alpha=0.3)
plt.subplot(1, 2, 2)
sorted_a = sorted(a)
ecdf = np.arange(1, n + 1) / n
plt.step(sorted_a, ecdf, where='post', label='Эмпирическая F(x)', color='blue')
x_theor = np.linspace(x_min, x_max, 100)
f_theor = 1 - np.exp(-l_z * x_theor)
plt.plot(x_theor, f_theor, label=f'Теоретическая F(x) (λ = {l_z:.2f})', color='red', linestyle='--')
plt.title("Функция распределения")
plt.xlabel("X")
plt.ylabel("F(X)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

