'''
title: prefix reversal - efficient algorithm assignment 1 
author: j. hu
date: 10.11.2024
target: a non-ordered array -> an ascending array
'''


def prefix_reversal_general(arr: list):
    '''
    a loop that 
    chooses the biggest element in arr[x: y] and records its index
    if the biggest element is not at the correct position(the end) 
    reverses arr[x: y] and move the biggest element to the end

    reference: 
        William H. Gate, C. H. Papadimitriou. BOUNDS FOR SORTING BY PREFIX REVERSAL. Discrete Mathematics 27, 47-57. 1979.
        especially Algorithm A & Fig 2

    reversal times: <= 2n
    '''
    if not arr:
        return []
    n = len(arr)

    res = []

    for right in range(n, 1, -1):

        biggest = max(arr[: right])
        biggest_index = arr[: right].index(biggest)
        
        # check if the biggest element is at the correct position(the end) 
        if biggest_index == right + 1:
            continue
        # 2 times reversal
        # 1. move biggest element to the head (optional)
        # 2. reversal the array for moving the biggest element to the end
        if biggest_index != 0:
            arr[: biggest_index + 1] = arr[: biggest_index + 1][:: -1]
            res.append(biggest_index)
        arr[: right] = arr[: right][:: -1]
        res.append(right - 1)

        # try to make a greedy search 
        # for more values such that are in the correct position
        while abs(arr[right - 2] - arr[right - 1]) == 1:
            right -= 1
    
    return arr, res, len(res)


def prefix_reversal_tritonic(arr: list):
    '''
    a loop that 
    by reversing the value, find the correct position from phase 2, 3 to phase 1
    begin with the second phase
    try to make a greedy reversal based on some sorted part

    reversal times: <= 3(n - a) (when a > 17)
    '''
    if not arr:
        return 
    res = []
    n = len(arr)
    a = 0
    while a + 1 < n and arr[a] < arr[a + 1]:
        a += 1
    b = a
    while b + 1 < n and arr[b] > arr[b + 1]:
        b += 1

    times = 0
    p = a + 1
    while p < n:
        greed = p
        # greedy search for a sorted part
        while greed + 1 < b and abs(arr[greed] - arr[greed + 1]) == 1:
            greed += 1 
        arr[: greed + 1] = arr[: greed + 1][::-1]
        res.append(greed)

        q = greed - p
        if times % 2:
            if q != 0 and arr[q] > arr[q - 1]:
                arr[: q + 1] = arr[: q + 1][::-1]
                res.append(q)
            while q + 1 < n and arr[greed - p] >= arr[q + 1]:
                # if it is the min value, it may over the boundary
                if p <= b and q == b:
                    break
                q += 1
            arr[: q + 1] = arr[: q + 1][::-1]
            res.append(q)
            if q != greed - p:
                arr[: q - greed + p] = arr[: q - greed + p][::-1]
                res.append(q - greed + p - 1)
        elif times % 2 == 0:
            if q != 0 and arr[q] < arr[q - 1]:
                arr[: q + 1] = arr[: q + 1][::-1]
                res.append(q)
            while q + 1 < n and arr[greed - p] < arr[q + 1]:
                # if it is the min value, it may over the boundary
                if p <= b and q == b:
                    break
                q += 1
            arr[: q + 1] = arr[: q + 1][::-1]
            res.append(q)
            if q != greed - p:
                arr[: q - greed + p] = arr[: q - greed + p][::-1]
                res.append(q - greed + p - 1)
        
        times += 1
        if greed != p:
            p = greed + 1
        else:
            p += 1

    if arr[0] > arr[1]:
        arr[:] = arr[:][::-1]
        res.append(n - 1)

    return arr, res


def prefix_reversal_binary(arr: list):
    '''
    a loop that when meeting 1, arr must reverses
    particularly pay attention to reversal times 

    idea:
        reverses when meeting 1

    reversal times: <= 2 * (nums of blocks of 1)
    '''
    if not arr:
        return 
    
    n = len(arr)
    times = 0
    
    res = []
    
    for i in range(n):
        if arr[i] == 0:
            continue
        
        if times != 0:
            # put all of 1 on the current end(based on i)
            arr = arr[: i][:: -1] + arr[i:]
            
            times += 1
            res.append(i - 1)
        
        # un-sorted but can be looked as a whole block of 1
        tmp = i
        while tmp + 1 < n and arr[tmp + 1] == 1:
            tmp += 1 
        arr[: tmp + 1] = arr[: tmp + 1][:: -1]
        times += 1
        res.append(tmp)

        i = tmp + 1
    
    # odd times reversal
    # all of 1 will be at the head, so needs to one more time reversal
    if times % 2:
        arr = arr[:][:: -1]
        res.append(n - 1)
    
    return arr, res    


def prefix_reversal_ternary(arr: list):
    '''
    a loop for ternary array sorting
    anyway, keep the blocks of 0, 1, 2

    idea:
        at first, regardless of the blocks order about {012}
        just focus on {xxx0}, {xxx1}, {xxx2}, totally 18 types:
        {0120}, {1020}, {0210}, {2010}, {2100}, {1200},
        {0121}, {2101}, {1201}, {1021}, {0211}, {2011},
        {1202}, {2102}, {2012}, {0212}, {1022}, {0122}
        in fact, when conditions about 00, 11, 22, that is
        {2100}, {1200}, {0211}, {2011}, {1022}, {0122},
        no any operations using on that. 
        only keep all same number pieces in the same block

        after the loop, the results have 6 possibilities:
        {012}, {021}, {102}, {120}, {201}, {210}
        
    reversal times: <= 2*(scattered and unordered blocks of 012)
    '''
    if not arr:
        return 
    res = []

    n = len(arr)
    for i in range(n):
        tmp = i
        if arr[i] == 0:
            while tmp < n - 1 and arr[tmp] == 0:
                tmp += 1
            if i == 0 or arr[i - 1] == 0:
                i = tmp + 1
                continue
            elif arr[i - 1] == 1:
                tmp_one = i - 1
                while tmp_one > 0 and arr[tmp_one] == 1:
                    tmp_one -= 1
                if arr[tmp_one] == 0:
                    # {2010}
                    arr[: tmp_one + 1] = arr[: tmp_one + 1][:: -1]
                    res.append(tmp_one)
                # {0210}
                arr[: i] = arr[: i][:: -1]
                res.append(i - 1)
            elif arr[i - 1] == 2:
                tmp_two = i - 1
                while tmp_two > 0 and arr[tmp_two] == 2:
                    tmp_two -= 1
                if arr[tmp_two] == 0:
                    # {1020}
                    arr[: tmp_two + 1] = arr[: tmp_two + 1][:: -1]
                    res.append(tmp_two)
                # {0120}
                arr[: i] = arr[: i][:: -1]
                res.append(i - 1)
        elif arr[i] == 1:
            while tmp < n - 1 and arr[tmp] == 1:
                tmp += 1
            if i == 0 or arr[i - 1] == 1:
                i = tmp + 1
                continue
            elif arr[i - 1] == 0:
                tmp_zero = i - 1
                while tmp_zero > 0 and arr[tmp_zero] == 0:
                    tmp_zero -= 1
                if arr[tmp_zero] == 1:
                    # {2101}
                    arr[: tmp_zero + 1] = arr[: tmp_zero + 1][:: -1]
                    res.append(tmp_zero)
                # {1201}
                arr[: i] = arr[: i][:: -1]
                res.append(i - 1) 
            elif arr[i - 1] == 2:
                tmp_two = i - 1
                while tmp_two > 0 and arr[tmp_two] == 2:
                    tmp_two -= 1
                if arr[tmp_two] == 1:
                    # {0121}
                    arr[: tmp_two + 1] = arr[: tmp_two + 1][:: -1]
                    res.append(tmp_two)
                # {1021}
                arr[: i] = arr[: i][:: -1]
                res.append(i - 1)
        elif arr[i] == 2:
            while tmp < n - 1 and arr[tmp] == 2:
                tmp += 1
            if i == 0 or arr[i - 1] == 2:
                i = tmp + 1
                continue
            elif arr[i - 1] == 0:
                tmp_zero = i - 1
                while tmp_zero > 0 and arr[tmp_zero] == 0:
                    tmp_zero -= 1
                if arr[tmp_zero] == 2:
                    # {1202}
                    arr[: tmp_zero + 1] = arr[: tmp_zero + 1][:: -1]
                    res.append(tmp_zero)
                # {2102}
                arr[: i] = arr[: i][:: -1]
                res.append(i - 1)
            elif arr[i - 1] == 1:
                tmp_one = i - 1
                while tmp_one > 0 and arr[tmp_one] == 1:
                    tmp_one -= 1
                if arr[tmp_one] == 2:
                    # {0212}
                    arr[: tmp_one + 1] = arr[: tmp_one + 1][:: -1]
                    res.append(tmp_one)
                # {2012}
                arr[: i] = arr[: i][:: -1]
                res.append(i - 1)
        i = tmp + 1
    
    # last handle
    if arr[0] == 0:
        index_1 = arr.index(1)
        index_2 = arr.index(2)
        # {012} is fine, so only handle with {021}
        if index_1 > index_2:
            arr[: index_1] = arr[: index_1][:: -1]
            arr = arr[:][::-1]
            tmp = arr.index(2)
            arr[: tmp] = arr[: tmp][:: -1]
            res.extend([index_1 - 1, n - 1, tmp - 1])
    elif arr[0] == 1:
        index_0 = arr.index(0)
        index_2 = arr.index(2)
        # {102}
        if index_0 < index_2:
            arr[: index_2] = arr[: index_2][:: -1]
            res.append(index_2 - 1)
        # {120}
        elif index_0 > index_2:
            arr[: index_0] = arr[: index_0][:: -1]
            arr = arr[:][::-1]
            res.extend([index_0 - 1, n - 1])
    elif arr[0] == 2:
        index_0 = arr.index(0)
        index_1 = arr.index(1)
        # {201}
        if index_0 < index_1:
            arr = arr[:][:: -1]
            tmp = arr.index(2)
            arr[: tmp] = arr[: tmp][:: -1]
            res.extend([n - 1, tmp - 1])
        # {210}
        elif index_0 > index_1:
            arr = arr[:][:: -1]
            res.append(n - 1)

    return arr, res


if __name__  == "__main__":
    # arr =  [44, 2, 29, 15, 37, 13, 1, 28, 48, 8, 34, 35, 21, 50, 6, 39, 12, 24, 41, 16, 11, 22, 47, 4, 10, 5, 42, 43, 40, 18, 30, 46, 7, 36, 19, 9, 45, 14, 38, 23, 31, 20, 26, 32, 33, 17, 3, 27, 49, 25]
    # print(prefix_reversal_general(arr))

    # arr = [1, 2, 3, 10, 14, 15, 17, 19, 20, 27, 28, 30, 31, 33, 35, 38, 40, 41, 44, 45, 46, 47, 49, 50, 48, 43, 42, 37, 36, 34, 32, 29, 25, 24, 23, 21, 18, 16, 13, 11, 9, 8, 6, 5, 4, 7, 12, 22, 26, 39]
    # arr =  [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 18, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 48, 49, 50, 34, 16, 2, 13, 14, 17, 19, 25, 33, 46, 47]
    arr = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 42, 45, 46, 47, 48, 49, 44, 41, 21, 16, 1, 2, 3, 22, 23, 34, 43, 50]
    # arr = [6, 19, 35, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    print(prefix_reversal_tritonic(arr))
    
    # arr = [0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0]
    # arr = [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1]
    # print(prefix_reversal_binary(arr))

    # arr =[1, 1, 2, 0, 2, 2, 2, 0, 2, 0, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 2, 0, 0, 0, 2, 0, 1, 1, 2, 1, 0, 2, 2, 1, 1, 2, 1, 2, 1, 0, 1, 1, 2, 2, 1, 1, 2, 0, 1, 1]
    # arr = [2, 0, 1]
    # print(prefix_reversal_ternary(arr))
