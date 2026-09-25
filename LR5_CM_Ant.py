import math
import random
import matplotlib.pyplot as plt

def get_test_data():
    """Возвращает список координат (x, y) из вашего примера"""
    raw_data = """
    1 37 52 7 
    2 49 49 30 
    3 52 64 16 
    4 20 26 9 
    5 40 30 21 
    6 21 47 15 
    7 17 63 19 
    8 31 62 23 
    9 52 33 11 
    10 51 21 5 
    11 42 41 19 
    12 31 32 29 
    13 5 25 23 
    14 12 42 21 
    15 36 16 10 
    16 52 41 15 
    17 27 23 3 
    18 17 33 41 
    19 13 13 9 
    20 57 58 28 
    21 62 42 8 
    22 42 57 8 
    23 16 57 16 
    24 8 52 10 
    25 7 38 28 
    26 27 68 7 
    27 30 48 15 
    28 43 67 14 
    29 58 48 6 
    30 58 27 19 
    31 37 69 11 
    32 38 46 12 
    33 46 10 23 
    34 61 33 26 
    35 62 63 17 
    36 63 69 6 
    37 32 22 9 
    38 45 35 15 
    39 59 15 14 
    40 5 6 7 
    41 10 17 27 
    42 21 10 13 
    43 5 64 11 
    44 30 15 16 
    45 39 10 10 
    46 32 39 5 
    47 25 32 25 
    48 25 55 17 
    49 48 28 18 
    50 56 37 10 
    """
    cities = []
    for line in raw_data.strip().split('\n'):
        parts = line.split()
        x, y = float(parts[1]), float(parts[2])
        cities.append((x, y))
    return cities


# -----------------------------------------------------------------------------
# 2. Загрузка данных я
def loadData(source):
    return get_test_data()


# -----------------------------------------------------------------------------
# 3. Матрица расстояний (2D)
# -----------------------------------------------------------------------------
def createMatrix(cities):
    n = len(cities)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = float('inf')
        for j in range(i):
            # ЕВКЛИДОВО РАССТОЯНИЕ 2D (X, Y)
            d = math.sqrt((cities[i][0] - cities[j][0]) ** 2 +
                          (cities[i][1] - cities[j][1]) ** 2)
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix


# -----------------------------------------------------------------------------
# 4. Длина маршрута
# -----------------------------------------------------------------------------
def tourLength(tour, matrix):
    total = 0
    for i in range(len(tour) - 1):
        total += matrix[tour[i]][tour[i + 1]]
    total += matrix[tour[-1]][tour[0]]  # возврат в начальный город
    return total


# -----------------------------------------------------------------------------
# 5. Построение решения муравьем
# -----------------------------------------------------------------------------
def buildSolution(start, matrix, pheromone, alpha, beta):
    n = len(matrix)
    TL = [] # табу лист
    S = list(range(n)) # множество еще непомещ-х городов

    i = start
    TL.append(i)
    S.remove(i)

    while S:
        probs = [] #город и вероятность перехода в нем
        denom = 0.0 #вычисление знаменателя - сумма по всем доступным городам
        # l выражения tau^alpha * eta^beta
        for j in S:
            tau = pheromone[i][j] ** alpha
            eta = (1.0 / matrix[i][j]) ** beta
            denom += tau * eta

        for j in S:
            tau = pheromone[i][j] ** alpha
            eta = (1.0 / matrix[i][j]) ** beta
            probs.append((j, tau * eta / denom)) #вычисление ваероятности для каждого корода

        r = random.random()
        cumulative = 0.0
        j = probs[-1][0] #значение по умолчанию - последний город
        for city, prob in probs:
            cumulative += prob # Накапливаем сумму вероятностей, чтобы понять, в какой "сектор" рулетки попал шарик.
            if r <= cumulative:
                j = city
                break

        TL.append(j)
        S.remove(j)
        i = j

    return TL


# -----------------------------------------------------------------------------
# 6. Обновление феромонов
# -----------------------------------------------------------------------------
def updatePheromone(pheromone, tours, matrix, rho, Q):
    #rho - коэффициент испарения феромона
    n = len(pheromone)

    for i in range(n):
        for j in range(n):
            pheromone[i][j] *= (1 - rho)

    for tour in tours: #добавление феромона от каждого муравья
        length = tourLength(tour, matrix)
        if length == 0: continue
        delta = Q / length # вклад одного муравья в каждое ребро тура
        for k in range(len(tour) - 1):
            i, j = tour[k], tour[k + 1]
            pheromone[i][j] += delta
            pheromone[j][i] += delta

        pheromone[tour[-1]][tour[0]] += delta
        pheromone[tour[0]][tour[-1]] += delta


# -----------------------------------------------------------------------------
# 7. ВИЗУАЛИЗАЦИЯ МАРШРУТА
# -----------------------------------------------------------------------------
def plot_route(cities, tour, length):
    """
    Построение графика маршрута
    """
    # Извлекаем координаты городов в порядке обхода
    x_coords = [cities[i][0] for i in tour]
    y_coords = [cities[i][1] for i in tour]

    # Добавляем первый город в конец для замыкания маршрута
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])

    # Создаем фигуру
    plt.figure(figsize=(12, 8))

    # Рисуем маршрут
    plt.plot(x_coords, y_coords, 'b-o', linewidth=1.5, markersize=6, label='Маршрут')


    start_x = cities[tour[0]][0]
    start_y = cities[tour[0]][1]
    plt.plot(start_x, start_y, 'ro', markersize=15, label='Начало маршрута', zorder=5)

    # Нумеруем города
    for i, (x, y) in enumerate(zip(x_coords[:-1], y_coords[:-1])):
        plt.annotate(str(i + 1), (x, y), fontsize=8, ha='right', va='bottom')

    # Настройки графика
    plt.title(f'Лучший найденный маршрут (длина: {length:.2f})', fontsize=12, fontweight='bold')
    plt.xlabel('X координата', fontsize=10)
    plt.ylabel('Y координата', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axis('equal')

    # Показываем график
    plt.tight_layout()
    plt.show()


# -----------------------------------------------------------------------------
# 8. Основной алгоритм
# -----------------------------------------------------------------------------
def antSystem(data_source, m, iterations, alpha, beta, rho, Q, tau0, verbose):
    cities = loadData(data_source)
    n = len(cities)
    matrix = createMatrix(cities)

    pheromone = [[tau0] * n for _ in range(n)]

    bestTour = None
    bestLength = float('inf')

    for iteration in range(1, iterations + 1):
        tours = []

        for k in range(m):
            start = random.randint(0, n - 1)
            tour = buildSolution(start, matrix, pheromone, alpha, beta)
            tours.append(tour)

            length = tourLength(tour, matrix)

            if length < bestLength:
                bestLength = length
                bestTour = tour[:]

        updatePheromone(pheromone, tours, matrix, rho, Q)

        if verbose and iteration % 10 == 0:
            print(f"Итерация {iteration:4d}: лучший маршрут = {bestLength:.2f}")

    print()
    print("---- Результат ----")
    S_out = [x + 1 for x in bestTour]
    S_out.append(S_out[0])
    print(f"Лучший маршрут: {S_out}")
    print(f"Минимальное расстояние: {bestLength:.2f}")

    # Построение графика маршрута
    plot_route(cities, bestTour, bestLength)

    return bestLength


# -----------------------------------------------------------------------------
# ЗАПУСК
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Вариант 1: Использовать встроенные тестовые данные
    data_source = "test_data"

    antSystem(
        data_source,
        m=30,  # Количество муравьев
        iterations=1000,  # Количество итераций
        alpha=1.0,
        beta=2.0,
        rho=0.1,  # Коэффициент испарения
        Q=1.0,  # Константа феромона
        tau0=0.1,
        verbose=True
    )