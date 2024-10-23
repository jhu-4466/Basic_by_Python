'''
title: prefix reversal - efficient algorithm assignment 1 
author: j. hu
date: 23.10.2024
target: a non-ordered array -> an ascending array
'''


def prefix_reversal(a: list):
    '''
    a loop that 
    chooses the biggest element in a[x: y] and records its index
    if the biggest element is not at the correct position(the end) 
    reverses a[x: y] and move the biggest element to the end

    reference: 
        William H. Gate, C. H. Papadimitriou. BOUNDS FOR SORTING BY PREFIX REVERSAL. Discrete Mathematics 27, 47-57. 1979.

    running time: O(2n + 3)
    '''
    n = len(a)
    res = []

    if not a:
        return 

    for right in range(n, 1, -1):  # O(n)
        biggest = max(a[: right])  # O(n)
        biggest_index = a[: right].index(biggest)  # O(n)
        
        # check if the biggest element is at the correct position(the end) 
        if biggest_index == right + 1:
            continue
        
        res.append(biggest_index)

        # 2 times reversal
        # 1. move biggest element to the head
        # 2. reversal the array for moving the biggest element to the end
        a[: right] = a[: biggest_index + 1][:: -1] + a[biggest_index + 1: right]
        a[: right] = a[: right][:: -1]
    
    return a, res
    


if __name__  == "__main__":
    a = [44, 2, 29, 15, 37, 13, 1, 28, 48, 8, 34, 35, 21, 50, 6, 39, 12, 24, 41, 16, 11, 22, 47, 4, 10, 5, 42, 43, 40, 18, 30, 46, 7, 36, 19, 9, 45, 14, 38, 23, 31, 20, 26, 32, 33, 17, 3, 27, 49, 25]

    print(prefix_reversal(a))
