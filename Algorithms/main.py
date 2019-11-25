import math
import xlwt
import random
import time
import os
import getch

def less(a, b):
    if det(a, b) > 0 or (det(a,b)==0 and a[0]**2+a[1]**2 < b[0]**2+b[1]**2):
        return True
    else:
        return False

def heapify(arr, i, hsize):
    largest = i
    right = 2*i + 2
    left = 2*i + 1
    if left < hsize and less(arr[largest], arr[left]):
        largest = left
    if right < hsize and less(arr[largest], arr[right]):
        largest = right
    if largest != i:
        arr[largest], arr[i] = arr[i], arr[largest]
        heapify(arr, largest, hsize)


def heapSort(arr):
    n = len(arr)

    for i in range(n//2, -1, -1):
        heapify(arr, i, n)
    
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, 0, i)

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        left = arr[:mid]
        right = arr[mid:]

        mergeSort(left)
        mergeSort(right)

        i=0
        j=0
        k=0
        while i<len(left) and j<len(right):
            if less(left[i], right[j]):
                arr[k]=left[i]
                i=i+1
            else:
                arr[k]=right[j]
                j=j+1
            k=k+1

        while i<len(left):
            arr[k]=left[i]
            i=i+1
            k=k+1

        while j<len(right):
            arr[k]=right[j]
            j=j+1
            k=k+1

def det(a, b):
    return (a[0]*b[1]) - (a[1]*b[0])

def findConv(a, sortfunc):
    n = len(a)
    c = min(a).copy()
    m = a.index(c)
    a[0], a[m] = a[m], a[0]
    m = 0
    for elem in a:
        elem[0] = elem[0] - c[0]
        elem[1] = elem[1] - c[1]
    sortfunc(a)
    if len(a) >= 2:
        stack = [a[0], a[1]]
    else:
        stack = [a[0]]
    for i in range(2, n):
        while len(stack)>1 and det((stack[-1][0]-stack[-2][0], stack[-1][1]-stack[-2][1]),
        (a[i][0]-stack[-1][0], a[i][1]-stack[-1][1])) < 0:
            stack.pop()
        stack.append(a[i])
    for elem in stack:
        elem[0] = elem[0] + c[0]
        elem[1] = elem[1] + c[1]
    return stack

def genPoints(n, q, w, mode):
    if mode == "1":
        start_posx = random.randint(0, 100)
        start_posy = random.randint(0, 100)
        points = list()
        for i in range(n):
            points.append([random.randint(start_posx, start_posx+q), random.randint(start_posy, start_posy+w)])
        return points
    if mode == "2":
        start_posx = random.randint(0, 100)
        start_posy = random.randint(0, 100)
        points = list()
        for i in range(n):
            x = random.randint(start_posx, start_posx + q)
            if x == start_posx or x == start_posx + q:
                y = random.randint(start_posy, start_posy + w)
                points.append([x, y])
            else:
                y = random.choice([start_posy, start_posy+w])
                points.append([x, y])
        return points


def main():
    PROGRAM_NOT_FINISHED = 1
    while PROGRAM_NOT_FINISHED:
        os.system("clear")
        print("----------------FINDING CONVEX HULL PROGRAM----------------")
        print("1.Указать количество точек")
        print("2.Указать q и w для псевдослучайного размещения")
        print("3.Сгенерировать точки")
        print("4.Построить выпуклую оболочку")
        print("5.Автоматическая генерация и запуск эксперимента")
        print("6.Завершить программу")
        key = getch.getch()
        if key == "1":
            os.system("clear")
            print("----------------FINDING CONVEX HULL PROGRAM----------------")
            n = abs(int(input("Введите число точек: ")))
        elif key == "2":
            os.system("clear")
            print("----------------FINDING CONVEX HULL PROGRAM----------------")
            q = abs(int(input("Введите q: ")))
            w = abs(int(input("Введите w: ")))
            os.system("clear")
            print("----------------FINDING CONVEX HULL PROGRAM----------------")
            print("Выберите режим размещения")
            print("1.В прямоугольнике со сторонами q и w")
            print("2.На границе этого прямоугольника")
            rand_mode = getch.getch()
        elif key == "3":
            os.system("clear")
            print("----------------FINDING CONVEX HULL PROGRAM----------------")
            print("Generating points...")
            arr = genPoints(n, q, w, rand_mode)
            os.system("clear")
            print("----------------FINDING CONVEX HULL PROGRAM----------------")
            if len(arr) <= 10:
                print("Points:", *arr)
            print("Points generated!")
            print("Нажмите любую клавишу, чтобы продолжить...")
            key = getch.getch()
        elif key == "4":
            os.system("clear")
            print("----------------FINDING CONVEX HULL PROGRAM----------------")
            try:
                print("n=", len(arr))
                print("q=", q)
                print("w=", w)
            except Exception:
                print("Ошибка ввода!\nНажмите любую клавишу, чтобы продолжить")
                getch.getch()
                continue
            print("Выберите алгоритм сортировки")
            print("1.Сортировка с помощью 2-кучи")
            print("2.Сортировка слиянием")
            print("3.Оба метода")
            sort_key = getch.getch()
            if sort_key == "1":
                t = time.time()
                print("Finding convex...")
                convex = findConv(arr.copy(), heapSort)
                t = time.time() - t
                print("CONVEX: ", *convex)
                print("Time: ", t, " seconds")
            elif sort_key == "2":
                t = time.time()
                print("Finding convex...")
                convex = findConv(arr.copy(), mergeSort)
                t = time.time() - t
                print("CONVEX: ", *convex)
                print("Time:", t, "seconds")
            elif sort_key == "3":
                t = time.time()
                print("Finding convex, heap sort...")
                convex = findConv(arr.copy(), heapSort)
                t = time.time() - t
                if n <= 10:
                    print("CONVEX_Heap:", *convex)
                print("Time_Heap:", t, "seconds")
                t = time.time()
                print("Finding convex, merge sort...")
                convex = findConv(arr.copy(), mergeSort)
                t = time.time() - t
                if n <= 10:
                    print("CONVEX_Merge:", *convex)
                print("Time_Merge:", t, "seconds")
            print("Нажмите любую клавишу, чтобы продолжить...")
            key = getch.getch()
        elif key == "5":
            os.system("clear")
            print("----------------FINDING CONVEX HULL PROGRAM----------------")
            book = xlwt.Workbook()
            ws1 = book.add_sheet("Exp1")
            ws1.write(0, 0, "N")
            ws1.write(0, 1, "TimeMerge")
            ws1.write(0, 2, "TimeHeap")
            ws2 = book.add_sheet("Exp2")
            ws2.write(0, 0, "Q, W")
            ws2.write(0, 1, "TimeMerge")
            ws2.write(0, 2, "TimeHeap")
            ws3 = book.add_sheet("Exp3")
            ws3.write(0, 0, "Q, W")
            ws3.write(0, 1, "TimeMerge")
            ws3.write(0, 2, "TimeHeap")
            q = 10000
            w = 10000
            n = 1
            i = 1
            print("Эксперимент 1: q = 10 000, w = 10 000, n = 1...100001 Шаг = 1000")
            while n <= 100001:
                print("Пожалуйста, подождите...", int((n/100001)*100), "%", end='\r')
                ws1.write(i, 0, n)
                arr = genPoints(n, q, w, "1")
                t = time.time()
                findConv(arr.copy(), mergeSort)
                ws1.write(i, 1, time.time()-t)
                t = time.time()
                findConv(arr.copy(), heapSort)
                ws1.write(i, 2, time.time()-t)
                i += 1
                n += 1000
            n = 100000
            q = w = 0
            i = 1
            print("Эксперимент 2: q = w = 0...10 000 внутри прямоугольника, Шаг = 100, n = 100000")
            while q <= 10000:
                print("Пожалуйста, подождите...", int((q/10000)*100), "%", end='\r')
                ws2.write(i, 0, q)
                arr = genPoints(n, q, w, "1")
                t = time.time()
                findConv(arr.copy(), mergeSort)
                ws2.write(i, 1, time.time()-t)
                t = time.time()
                findConv(arr.copy(), heapSort)
                ws2.write(i, 2, time.time()-t)
                i += 1
                q += 100
                w += 100
            n = 100000
            q = w = 0
            i = 1
            print("Эксперимент 3: q = w = 0...10 000 на сторонах прямоугольника, Шаг = 100, n = 100000")
            while q <= 10000:
                print("Пожалуйста, подождите...", int((q/10000)*100), "%", end='\r')
                ws3.write(i, 0, q)
                arr = genPoints(n, q, w, "2")
                t = time.time()
                findConv(arr.copy(), mergeSort)
                ws3.write(i, 1, time.time()-t)
                t = time.time()
                findConv(arr.copy(), heapSort)
                ws3.write(i, 2, time.time()-t)
                i += 1
                q += 100
                w += 100
            print("Сохраняю в experiment.xls")
            book.save("experiment.xls")
            print("Нажмите любую клавишу, чтобы продолжить...")
            key = getch.getch()
                
        elif key == "6":
            PROGRAM_NOT_FINISHED = 0


if __name__ == "__main__":
    main()

