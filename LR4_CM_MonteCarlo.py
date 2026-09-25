import random
import math

def f(x):
    """Функция для интегрирования: f(x) = x^2 + 1"""
    return x**2 + 1

a = 1  # нижняя граница интервала
b = 3  # верхняя граница интервала
n = 50  # количество испытаний
confidence_level = 0.95  # доверительная вероятность (95%)



def monte_carlo_integration(f, a, b, n):
    """Вычисление интеграла методом Монте-Карло"""
    x_values = []
    f_values = []

    for i in range(n):
        u = random.uniform(0, 1)
        x = a + (b - a) * u
        fx = f(x)

        x_values.append(x)
        f_values.append(fx)

    omega = (b - a) * sum(f_values) / n

    return omega, x_values, f_values


def calculate_variance(f_values, omega, n):
    """Вычисление выборочной дисперсии"""
    sum_squared_diff = sum((fx - omega) ** 2 for fx in f_values)
    variance = sum_squared_diff / (n - 1)
    return variance


def confidence_interval(omega, variance, n, confidence_level):
    """Построение доверительного интервала"""
    S = math.sqrt(variance)

    if confidence_level == 0.95:
        Z = 1.96
    elif confidence_level == 0.90:
        Z = 1.64
    elif confidence_level == 0.99:
        Z = 2.576
    else:
        Z = 1.96

    margin = Z * (S / math.sqrt(n))

    return (omega - margin, omega + margin), Z, margin


def theoretical_integral(a, b):
    """
    Теоретическое значение интеграла от (x^2 + 1) на [a, b]
    ∫(x^2+1)dx = [x^3/3 + x] от a до b
    """

    def F(x):
        return (x ** 3)/3 +  x

    return F(b) - F(a)


# ================= ОСНОВНАЯ ПРОГРАММА =================


print("\nМетод Монте-Карло для вычисления интеграла")
print("=" * 60)
print(f"\nФункция: f(x) = x^2 + 1")
print(f"Интервал: [{a}, {b}]")
print(f"Количество испытаний: n = {n}")
print(f"Доверительная вероятность: {confidence_level * 100}%")


omega, x_values, f_values = monte_carlo_integration(f, a, b, n)
I_exact = theoretical_integral(a, b)
absolute_error = abs(I_exact - omega)
variance = calculate_variance(f_values, omega, n)
std_dev = math.sqrt(variance)
conf_int, Z, margin = confidence_interval(omega, variance, n, confidence_level)

print("\nРЕЗУЛЬТАТЫ ВЫЧИСЛЕНИЙ:")
print("-" * 60)
print(f"Оценка интеграла (ω):           {omega:.6f}")
print(f"Теоретическое значение (I):     {I_exact:.6f}")
print(f"Абсолютная погрешность |I-ω|:   {absolute_error:.6f}")
print(f"Выборочная дисперсия (S²):      {variance:.6f}")
#print(f"Стандартное отклонение (S):     {std_dev:.6f}")
print(f"\n{confidence_level * 100}% ДОВЕРИТЕЛЬНЫЙ ИНТЕРВАЛ:")
print(f"  Критическое значение Z:       {Z}")
print(f"  Полуширина интервала:         {margin:.6f}")
print(f"  Интервал:                     [{conf_int[0]:.6f}; {conf_int[1]:.6f}]")

if conf_int[0] <= I_exact <= conf_int[1]:
    print(f"\nТеоретическое значение {I_exact:.6f} попадает в доверительный интервал")
else:
    print(f"\nТеоретическое значение {I_exact:.6f} НЕ ПОПАДАЕТ в доверительный интервал")


print("\nИспытания:")
print("-" * 60)
print(f"{'№':<5} {'u_i':<10} {'x_i':<10} {'f(x_i)':<10}")
print("-" * 60)
for i in range( n):
    u = (x_values[i] - a) / (b - a)
    print(f"{i + 1:<5} {u:<10.4f} {x_values[i]:<10.4f} {f_values[i]:<10.4f}")

print("\n" + "=" * 60)