from random import uniform
import math

lambda_max = 7.9
# Неоднородная интенсивность входа (звонков в час)
lambda_by_hour = {
    8: 7.9, 9: 7.2, 10: 7.2, 11: 7.4,
    12: 7.5, 13: 7.3, 14: 7.1, 15: 7.6, 16: 7.3, 17: 7.1,
}
def get_lambda_t(t):
    hour = int(t // 60)
    if hour > 23: hour = 23 
    val_per_hour = lambda_by_hour.get(hour, 0.0)
    return val_per_hour / 60.0

def generate_exp(lambd):
    u = uniform(0, 1)
    return -math.log(1 - u) / lambd

def generate_poisson(t, lambda_t, lambda_max):
    while t <= T:
        u1 = uniform(0, 1)
        t = t - math.log(u1) / lambda_max
        if t <= T:
            u2 = uniform(0, 1)
            if u2 <= calc_lambda_t(lambda_t, t) / lambda_max:
                break
    return t

def cmo (T, lambda_t, lambda_exp):
    lambda_max = max([lambda_t[i][2] for i in range(len(lambda_t))]) #как это считается ?!?!
    INF = 1e9
    t = n = 0
    A = [] #  времена поступлений клиентов
    D = [] # времена ухода клиентов по завершении обслуживания D_i = A_i + W_i + V_i
    ta = generate_poisson(t, lambda_t, lambda_max) # время прибытия следующего клиента
    td = INF # время завершения работы устройства
    Q = 0 # число клиентов в момент времени t
    p = 0 # средний коэффициент занятости устройства
    N_a = 0 # число прибывших клиентов к моменту времени t
    N_d = 0 # число уходов клиентов к моменту времени t
    while True:
        if ta <= td and ta <= T: # прибытие клиента
            Q += n * (ta - t)
            p += (n > 0) * (ta - t)
            t = ta # время прибытия следующего клиента
            n += 1 # в настоящее время имеется более одного клиента
            N_a += 1
            Tt = generate_poisson(t, lambda_t, lambda_max) # время прибытия следующего клиента (ген Пуас)
            ta = Tt
            if n == 1:
                V = generate_exp(lambda_exp)
                td = t + V
            A.append(t) 
        if td < ta and td < T:
            Q += n * (td - t)
            p += (n > 0) * (td - t)
            t = td
            N_d += 1
            n = n - 1
            if n == 0:
                td = INF
            else:
                V = generate_exp(lambda_exp)
                td = t + V
            D.append(t)
        if min(ta, td) > T and n > 0: 
            t = td
            Nd = Nd + 1
            n = n - 1
            if n > 0:
                V = generate_exp(lambda_exp)
                td = t + V
                D.append(t)
        if min(ta, td) > T and n == 0:
            break
    return A, D

#Оценки для анализа СМО в течение интервала времени [0, T]
# St = 1/N(t) * sum (Di - Ai)
def S_t(A, D):
    return sum([D[i] - A[i] for i in range(len(A))]) / len(A)

#Оценка ожидаемой задержки клиентов
#Среднее по временам задержек
def W_t(A, D):
    return sum([max(0, D[i - 1] - A[i]) for i in range(1, len(A))]) / len(A)


#Поскольку n(t) меняется только в моменты приходов и уходов,

def expect_client_count(T, A, D):
    n = 0
    sm = 0
    prev = 0
    i = j = 0

    while i < len(A):
        sm += n * (min(A[i], D[j]) - prev)
        prev = min(A[i], D[j])
        if A[i] < D[j]:
            n += 1
            i += 1
        else:
            n -= 1
            j += 1
    while j < len(D) and D[j] <= T:
        sm += n * (min(D[j],T) - prev)
        prev = D[j]
        n -= 1
        j += 1
    sm += n * (T - prev)
    return sm / T

def occupancy_rate(T, A, D):
    n = 0
    sm = 0
    prev = 0
    i = j = 0

    while i < len(A):
        sm += (n > 0) * (min(A[i], D[j]) - prev)
        prev = min(A[i], D[j])
        if A[i] < D[j]:
            n += 1
            i += 1
        else:
            n -= 1
            j += 1

    while j < len(D) and D[j] <= T:
        sm += (n > 0) * (min(D[j],T) - prev)
        prev = D[j]
        n -= 1
        j += 1
    sm += (n > 0) * (T - prev)
    return sm / T


# расчет интервалов в файле СMOCMO (там и график)
