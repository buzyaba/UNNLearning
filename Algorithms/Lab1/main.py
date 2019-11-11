import math
import numpy
import random
import time

def heapify(arr, i, hsize):
    largest = i
    right = 2*i + 2
    left = 2*i + 1
    if left < hsize and arr[largest] < arr[left]:
        largest = left
    if right < hsize and arr[largest] < arr[right]:
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
            if left[i]<right[j]:
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


def main():
    mas = list(random.randint(-500000, 500000) for i in range(random.randint(10000, 1000000)))
    print("Array has been generated! Size is ", len(mas))
    print("Sorting...")
    a = time.time()
    heapSort(mas)
    print("Time of heap sort is ", time.time()-a)

if __name__ == "__main__":
    main()

