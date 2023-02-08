# Zeynep Baydemir - Fatma Sena Alci
# The pseudocodes in the lecture slides are used to implement the algorithms
import random
import timeit
import sys
import copy
import resource
# increases recursion limit to be able to execute with big inputs
# increases stack limit
resource.setrlimit(resource.RLIMIT_STACK, [0x10000000, resource.RLIM_INFINITY])
sys.setrecursionlimit(0x100000)



# Ver1
# classical version of the quick sort
# it chooses first element as pivot
# splits the list and calls the function recursively
def classical_quick_sort(lst, low, high):
    if low < high:
        position = rearrange_classical(lst, low, high)
        classical_quick_sort(lst, low, position-1)
        classical_quick_sort(lst, position+1, high)


# Finds the position to split the list
# Partitioning the other elements into two sublists based on whether they are less than or greater than the pivot
def rearrange_classical(lst, low, high):
    right = low + 1
    left = high
    pivot = lst[low]
    while right <= left:
        while right <= left and lst[right] <= pivot:
            right += 1
        while right <= left and lst[left] >= pivot:
            left -= 1
        if right <= left:
            lst[right], lst[left] = lst[left], lst[right]
    position = left
    lst[low], lst[position] = lst[position], pivot
    return position


# Ver2
# Chooses pivot randomly
# Partitioning the other elements into two sublists based on whether they are less than or greater than the pivot
def quick_sort_first_version(lst, low, high):
    if low < high:
        position = rearrange_first_version(lst, low, high)
        quick_sort_first_version(lst, low, position - 1)
        quick_sort_first_version(lst, position + 1, high)


def rearrange_first_version(lst, low, high):
    right = low
    left = high
    index = random.randint(low, high)
    pivot = lst[index]
    lst[index], lst[low] = lst[low], pivot
    while right <= left:
        while right <= left and lst[right] <= pivot:
            right += 1
        while right <= left and lst[left] >= pivot:
            left -= 1
        if right <= left:
            lst[right], lst[left] = lst[left], lst[right]
        else:
            break
    position = left
    lst[low], lst[position] = lst[position], lst[low]
    return position


# Ver3
# Randomly permutes the list
# Chooses pivot as first element as classical sort
# Partitioning the other elements into two sublists based on whether they are less than or greater than the pivot
def quick_sort_second_version(lst, low, high):
    for i in range(high-low-1):
        x = random.randint(0,high)
        lst[i], lst[x] = lst[x], lst[i]
    classical_quick_sort(lst, low, high)


# Ver4
# Uses median of three rule
# Partitioning the other elements into two sublists based on whether they are less than or greater than the pivot
def quick_sort_median(lst, low, high):
    if low < high:
        position = rearrange_median(lst, low, high)
        quick_sort_median(lst, low, position-1)
        quick_sort_median(lst, position+1, high)


# Pivot is median of first element, last element and middle element
def rearrange_median(lst, low, high):
    right = low
    left = high
    length = len(lst)
    ind = length // 2
    mid = lst[ind]
    pivot = median(lst[low], mid, lst[high])
    if pivot == lst[low]:
        index = low
    elif pivot == mid:
        index = ind
    else:
        index = high
    lst[index], lst[low] = lst[low], pivot
    while right <= left:
        while right <= left and lst[right] <= pivot:
            right += 1
        while right <= left and lst[left] >= pivot:
            left -= 1
        if right <= left:
            lst[right], lst[left] = lst[left], lst[right]
    position = left
    lst[low], lst[position] = lst[position], lst[low]
    return position


# Finds median of the three numbers
def median(low, mid, high):
    if (low > mid) and (mid > high):
        return mid

    elif (low > high) and (high > mid):
        return high

    elif (high > mid) and (mid > low):
        return mid

    elif (mid > high) and (high > low):
        return high

    else:
        if mid == high:
            return mid
        return low


# Input type 1
# Creates list with size n
# Elements are random numbers between 0 and 10*n
def input_type1(n):
    lst = [(random.randint(1, 10*n)) for i in range(n)]
    return lst


# Input type 2
# Creates list with size n
# Elements are random numbers between 0 and 0.75*n
def input_type2(n):
    lst = [(random.randint(1, 0.75*n)) for i in range(n)]
    return lst


# Input type 3
# Creates list with size n
# Elements are random numbers between 0 and 0.25*n
def input_type3(n):
    lst = [(random.randint(1, 0.25*n)) for i in range(n)]
    return lst


# Input type 4
# Creates list with size n
# Elements are all 1
def input_type4(n):
    lst = [1]*n
    return lst


f = open("out.txt", "w")

# Writes the element in the list with hyphens between elements to the the file
def hyphen(lst):
    last = 0
    for i in lst:
        if last < len(lst)-1:
            last += 1
            f.write(str(i)+"-")
        else: 
             f.write(str(i) + "\n")

# Copies the list to send the same list to different versions of quick sort
def copy_lst(n, input_type):
    lst = []
    ls = []
    worst = []
    # 5 different list for averages
    for i in range(5):
        if input_type == 1:
            random_list = input_type1(n)
            if i == 0:
                wrst = input_type1(n)
                classical_quick_sort(wrst, 0, n-1)
        elif input_type == 2:
            random_list = input_type2(n)
            if i == 0:
                wrst = input_type2(n)
                classical_quick_sort(wrst, 0, n-1)
        elif input_type == 3:
            random_list = input_type3(n)
            if i == 0:
                wrst = input_type3(n)
                classical_quick_sort(wrst, 0, n-1)
        else:
            random_list = input_type4(n)
            if i == 0:
                wrst = input_type4(n)
                classical_quick_sort(wrst, 0, n-1)

        f.write("Input" + str(i+1) + " (average)=")
        hyphen(random_list)

        lst.append(random_list)
    f.write("Input (worst)=")
    hyphen(wrst)
    # 4 copy of average lists
    for i in range(4):
        ls.append(copy.deepcopy(lst))
        worst.append(wrst)
    return ls, worst


input_size = [100,1000,10000]

# Calls versions of quick sort five times with different lists for each to measure average execution time and writes to a file
# Measures execution times for worst cases and writes to a file
def execution_time(input_type):
    f.write("\n")
    for n in input_size:
        lst, worst = copy_lst(n,input_type)
        time = 0
        # for classical sort
        for i in range(5):
            start = timeit.default_timer()
            classical_quick_sort(lst[0][i], 0, n-1)
            end = timeit.default_timer()
            time += (end-start)*1000
        f.write("Ver1 Average=")
        f.write((str)(time/5))
        f.write("ms\n")
    
        worst_time = 0
        start = timeit.default_timer()
        classical_quick_sort(worst[0], 0, n-1)
        end = timeit.default_timer()
        worst_time = (end-start)*1000
        f.write("Ver1 Worst=")
        f.write((str) (worst_time))
        f.write("ms\n")
        # for first version
        time = 0
        for i in range(5):
            start = timeit.default_timer()
            quick_sort_first_version(lst[1][i], 0, n-1)
            end = timeit.default_timer()
            time += (end - start) * 1000
        f.write("Ver2 Average=")
        f.write((str)(time/5))
        f.write("ms\n")
        worst_time = 0
        start2 = timeit.default_timer()
        quick_sort_first_version(worst[1], 0, n-1)
        end2 = timeit.default_timer()
        worst_time = (end2-start2)*1000
        f.write("Ver2 Worst=")
        f.write((str) (worst_time))
        f.write("ms\n")
        # for second version
        time = 0
        for i in range(5):
            start = timeit.default_timer()
            quick_sort_second_version(lst[2][i], 0, n - 1)
            end = timeit.default_timer()
            time += (end - start) * 1000
        f.write("Ver3 Average=")
        f.write((str)(time/5))
        f.write("ms\n")
        worst_time = 0
        start = timeit.default_timer()
        quick_sort_second_version(worst[2], 0, n-1)
        end = timeit.default_timer()
        worst_time = (end-start)*1000
        f.write("Ver3 Worst=")
        f.write((str) (worst_time))
        f.write("ms\n")
        # for median of three
        time = 0
        for i in range(5):
            start = timeit.default_timer()
            quick_sort_median(lst[3][i], 0, n-1)
            end = timeit.default_timer()
            time += (end - start) * 1000
        f.write("Ver4 Average=")
        f.write((str)(time/5))
        f.write("ms\n")
        worst_time = 0
        start1 = timeit.default_timer()
        quick_sort_median(worst[3], 0, n-1)
        end1 = timeit.default_timer()
        worst_time = (end1-start1)*1000
        f.write("Ver4 Worst=")
        f.write((str) (worst_time))
        f.write("ms\n")


# Writes execution times for each input type and writes to a file
f.write("InpType1")
execution_time(1)
f.write("InpType2")
execution_time(2)
f.write("InpType3")
execution_time(3)
f.write("InpType4")
execution_time(4)


