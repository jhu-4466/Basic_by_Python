'''
title: prefix reversal - efficient algorithm assignment 1 
author: j. hu
date: 22.10.2024
'''


def prefix_reversal_basic(a: list):
    '''
    a loop that 
    chooses the biggest element in a[x: y] and records its index
    reverses a[x: y] and move the biggest element to the end

    running time: O(n^2)
    '''
    n = len(a)

    if not a:
        return 

    for _ in range(n):  # O(n)
        biggest = max(a[: n - _])  # O(n)
        
        a[: n - _] = reversed(a[: n - _])  # O(n)

        biggest_index = a[: n - _].index(biggest)  # O(n)
        a[: n - _] = a[:biggest_index] + a[biggest_index + 1: n - _] + [biggest]  # O(n)
    
    return a


if __name__  == "__main__":
    a = [4, 3, 5, 6, 1, 2]

    print(prefix_reversal_basic(a))
