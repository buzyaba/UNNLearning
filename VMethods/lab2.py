import numpy as np
import getch
import os
import random
import math

EXIT_PROGRAM = 1

def inputList(number, message):
    print(message)
    res = []
    while (len(res) < number):
        tmp = input().split()
        for elem in tmp:
            try:
                val = float(elem)
            except ValueError:
                continue
            else:
                if (len(res) < number):
                    res.append(val)
                else:
                    break
    return res

def printMatrix(A, b):
    n = len(A)
    for i in range(n):
        for j in range(n):
            print(str(A.A[i][j])+"x"+str(j), end="")
            if j < n-1:
                print(" + ", end="")
        print(" =", b[i])

def gaussMethod(b, f):
    error1 = "СЛАУ имеет бесконечное множество решений"
    error2 = "СЛАУ не имеет решения"
    a = b.copy()
    y = f.copy()
    k, n = 0, len(a)
    t = 0
    x = np.array([0.0 for i in range(n)])
    while k < n:
        max = abs(a.A[k][k])
        index = k
        for i in range(k+1, n):
            if abs(a.A[i][k]) > max:
                max = abs(a.A[i][k])
                index = i
        if max == 0:
            if k == n-1:
                if y[k] != 0:
                    return error1
                else:
                    return error2
            else:
                for i in range(n):
                    t += a.A[k][i]
                if t == 0:
                    if y[k] != 0:
                        return error1
            k += 1
        else:
            if index != k:
                a.A[index], a.A[k] = a.A[k].copy(), a.A[index].copy()
                y[index], y[k] = y[k], y[index]
            for i in range(k, n):
                temp = a.A[i][k]
                if temp == 0:
                    continue
                for j in range(n):
                    a.A[i][j] = a.A[i][j] / temp
                y[i] = y[i] / temp
                if i == k:
                    continue
                for j in range(n):
                    a.A[i][j] = a.A[i][j] - a.A[k][j]
                y[i] = y[i] - y[k]
            k += 1
    for k in range(n-1, -1, -1):
        x[k] = round(y[k], 3)
        for i in range(n):
            y[i] = round(y[i] - a.A[i][k] * x[k], 3)
    return x

def kramerMethod(a, y):
    error1 = "СЛАУ имеет бесконечное множество решений"
    error2 = "СЛАУ не имеет решения"
    detC = []
    correct = 0
    n = len(a)
    x = np.array([0.0 for i in range(n)])
    for i in range(n):
        detC.append(GetDet(a, y, i))
    det = np.linalg.det(a)
    if det == 0:
        for i in range(n):
            correct += detC[i]
        if correct == 0:
            correct = 0
            for i in range(n):
                correct += y[i]
            if correct == 0:
                return error1
            else:
                return error2
        else:
            return error2
    else:
        for i in range(n):
            x[i] = round(detC[i] / det, 3)
    return x

def GetDet(a, y, j):
    n = len(a)
    b = a.copy()
    for i in range(n):
        b.A[i][j] = y[i]
    det = np.linalg.det(b)
    return det

def seidelMethod(A, b, eps=0.001):
    n = len(A)
    x = np.array([.0 for i in range(n)])
    converge = False
    for i in range(n):
        if A.A[i][i] == 0:
            converge = True
            x = np.array([])
            print("Метод не сходится")
            break
    while not converge:
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(A.A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A.A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A.A[i][i]
        if abs(x_new[0] - x[0]) > 100000:
            x = np.array([])
            print("Метод не сходится")
            break
        converge = math.sqrt(
            sum((x_new[i] - x[i]) ** 2 for i in range(n))) <= eps
        x = x_new
    for i in x:
        i = round(i, 3)
    return x

def check_symmetric(a, tol=1e-8):
    return np.all(np.abs(a-a.T) < tol)

def relaxMethod(A, b, eps=0.001, omega=1.5):
    n = len(A)
    x = np.array([.0 for i in range(n)])
    converge = False
    if not converge:
        for i in range(n):
            if A.A[i][i] == 0:
                converge = True
                x = np.array([])
                print("Метод не сходится")
                break
    while not converge:
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(A.A[i][j] * x_new[j] * omega for j in range(i))
            s2 = sum(A.A[i][j] * x[j] * omega for j in range(i + 1, n))
            x_new[i] = (b[i] * omega - s1 - s2) / A.A[i][i] - x[i]*(omega - 1)
        if abs(x_new[0] - x[0]) > 100000:
            x = np.array([])
            print("Метод не сходится")
            break
        converge = math.sqrt(
            sum((x_new[i] - x[i]) ** 2 for i in range(n))) <= eps
        x = x_new
    for i in x:
        i = round(i, 3)
    return x

def simpleIterationMethod(mat, f):
    precision = 1e-5
    if 0 in mat.diagonal().A[0]:
        print("Главная диагональ с нулевыми элементами")
        return np.array([])
    diag = mat.diagonal().A.copy()[0]
    A = mat.A.copy()
    for i in range(n):
        temp = diag[i]
        f[i] /= temp
        for j in range(n):
            if i == j:
                A[i][j] = 0
            else:
                A[i][j] /= temp
    norm = np.linalg.norm(A, np.inf)
    if norm >= 1:
        print("Нет диагонального преобладания")
        return np.array([])
    xnew = f.copy()
    xold = f.copy()
    while True:
        xold = xnew
        xnew = f.copy()
        norm = 0
        for i in range(n):
            for j in range(n):
                xnew[i] -= A[i][j] * xold[j]
            if abs(xnew[i]-xold[i]) > norm:
                norm = abs(xnew[i]-xold[i])
        if norm <= precision:
            break
    for i in xnew:
        i = round(i, 3)
    return xnew

def LU(mat, f):
    if np.linalg.det(mat) == 0:
        print("Матрица вырожденная, решение методом LU-разложение невозможно")
        return np.array([])
    A = np.matrix(mat.A.copy())
    n = len(A.A)
    L = np.matrix([[0.0]*n for i in range(n)])
    U = np.matrix([[0.0]*n for i in range(n)])
    x = np.array([0.0 for i in range(n)])
    y = np.array([0.0 for i in range(n)])
    for i in range(n):
        for j in range(i, n):
            L.A[j][i] = A.A[j][i] - sum(L.A[j][k]*U.A[k][i] for k in range(j))
            U.A[i][j] = (A.A[i][j] - sum(L.A[i][k]*U.A[k][j] for k in range(i)))/L.A[i][i]
    for i in range(n):
        y[i] = (f[i]-sum(L.A[i][k]*y[k] for k in range(i)))/L.A[i][i]
    for i in range(n-1, -1, -1):
        s = sum(U.A[i][k]*x[k] for k in range(n-1, i-1, -1))
        x[i] = y[i] - s
    for i in range(n):
        x[i] = round(x[i], 3)
    return x

def thomasAlg(a, b, c, d):
    nf = len(d)  # number of equations
    ac, bc, cc, dc = map(np.array, (a, b, c, d))  # copy arrays
    for it in range(1, nf):
        mc = ac[it-1]/bc[it-1]
        bc[it] = bc[it] - mc*cc[it-1]
        dc[it] = dc[it] - mc*dc[it-1]

    xc = bc
    xc[-1] = dc[-1]/bc[-1]

    for il in range(nf-2, -1, -1):
        xc[il] = (dc[il]-cc[il]*xc[il+1])/bc[il]

    return xc

if __name__ == "__main__":
    while EXIT_PROGRAM == 1:
        os.system("clear")
        print("-----------------SOLVING SYSTEMS OF LINEAR EQUATIONS-----------------")
        print("1.Генерация СЛАУ")
        print("2.Метод Гаусса")
        print("3.Метод Крамера")
        print("4.Метод Зейделя")
        print("5.Метод верхних релаксаций")
        print("6.Метод простых итераций")
        print("7.Метод LU-разложения")
        print("8.Метод прогонки")
        print("9.Выйти из программы")
        key = getch.getch()
        if key == "1":
            os.system("clear")
            print("-----------------SOLVING SYSTEMS OF LINEAR EQUATIONS-----------------")
            n = int(input("Введите размер матрицы:"))
            print("1.Случайная генерация\n2.Ввод вручную")
            key = getch.getch()
            if key == "1":
                mat = np.matrix([[round(random.uniform(0, 100), 1) for i in range(n)] for j in range(n)])
                b = np.array([round(random.uniform(0, 100), 1) for i in range(n)])
            elif key == "2":
                tmp = inputList(n * n, "Input A matrix: ")
                mat = np.matrix([[tmp[i*n + j] for j in range(n)] for i in range(n)])
                b = np.array(inputList(n, "Input b: "))
            printMatrix(mat, b)
            print("Нажмите любую клавишу...")
            getch.getch()
        elif key == "2":
            os.system("clear")
            print("-----------------SOLVING SYSTEMS OF LINEAR EQUATIONS-----------------")
            printMatrix(mat, b)
            x = gaussMethod(mat, b.copy())
            print(x)
            print("Нажмите любую клавишу...")
            getch.getch()
        elif key == "3":
            os.system("clear")
            print("-----------------SOLVING SYSTEMS OF LINEAR EQUATIONS-----------------")
            printMatrix(mat, b)
            x = kramerMethod(mat, b.copy())
            print(x)
            print("Нажмите любую клавишу...")
            getch.getch()
        elif key == "4":
            os.system("clear")
            print("-----------------SOLVING SYSTEMS OF LINEAR EQUATIONS-----------------")
            printMatrix(mat, b)
            x = seidelMethod(mat, b.copy())
            print(*x)
            print("Нажмите любую клавишу...")
            getch.getch()
        elif key == "5":
            os.system("clear")
            print("-----------------SOLVING SYSTEMS OF LINEAR EQUATIONS-----------------")
            printMatrix(mat, b)
            x = relaxMethod(mat, b.copy())
            print(*x)
            print("Нажмите любую клавишу...")
            getch.getch()
        elif key == "6":
            os.system("clear")
            print("-----------------SOLVING SYSTEMS OF LINEAR EQUATIONS-----------------")
            printMatrix(mat, b)
            x = simpleIterationMethod(mat, b.copy())
            print(*x)
            print("Нажмите любую клавишу...")
            getch.getch()
        elif key == "7":
            os.system("clear")
            print("-----------------SOLVING SYSTEMS OF LINEAR EQUATIONS-----------------")
            printMatrix(mat, b)
            x = LU(mat, b)
            print(*x)
            print("Нажмите любую клавишу...")
            getch.getch()
        elif key == "8":
            os.system("clear")
            print("-----------------SOLVING SYSTEMS OF LINEAR EQUATIONS-----------------")
            printMatrix(mat, b)
            x = thomasAlg(mat.A.diagonal(-1), mat.A.diagonal(0), mat.A.diagonal(1), b.copy())
            print(x)
            print("Нажмите любую клавишу...")
            getch.getch()
        elif key == "9":
            EXIT_PROGRAM = 0
        