import random
import time
from math import floor


def example(arr):
    n = len(arr)
    arr2 = [0, 0, 0, 0, 0]
    for i in range(n):
        if arr[i] == 0:
            t1 = i
            for t1 in range(n):
                p1 = t1 ** (1 / 2)
                x1 = n + 1
                while x1 >= 1:
                    x1 = floor(x1 / 2)
                    arr2[i % 5] += 1
        elif arr[i] == 1:
            for t2 in range(n, 0, -1):
                for p2 in range(n):
                    x2 = n + 1
                    while x2 > 0:
                        x2 = floor(x2 / 2)
                        arr2[i % 5] += 1

        elif arr[i] == 2:
            for t3 in range(1, n + 1):
                x3 = t3 + 1
                for p3 in range(0, (t3 ** 2)):
                    arr2[i % 5] += 1
    return arr2


input_size = [1, 5, 10, 25, 50, 75, 100, 150, 200, 250]
time_elapsed = [[], [], []]
sample_array = [[], [], []]
for t in input_size:
    sample_array[0] = [0]*t #best
    sample_array[1] = []
    for j in range(t): #avg
        sample_array[1].append(random.randint(0,2))
    sample_array[2] = [2] * t  # worst

    for k in range(3):
        start = time.time()
        example(sample_array[k])
        end = time.time()
        time_elapsed[k].append((end-start)*10**3)
        if k == 0:
            print("Case: best Size: " + str(t) + " Elapsed Time: " + str((end-start)*10**3))
        if k == 1:
            print("Case: average Size: " + str(t) + " Elapsed Time: " + str((end-start)*10**3))
        if k == 2:
            print("Case: worst Size: " + str(t) + " Elapsed Time: " + str((end-start)*10**3))

