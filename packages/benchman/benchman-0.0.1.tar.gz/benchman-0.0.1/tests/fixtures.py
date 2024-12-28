# (c) 2024 Martin Wendt; see https://github.com/mar10/benchman
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
from random import randint
from typing import Any

SMALL_RANDOM_ARRAY = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
MEDIUM_RANDOM_ARRAY = [randint(0, 100) for _ in range(100)]
LARGE_RANDOM_ARRAY = [randint(0, 1000) for _ in range(1000)]


def quick_sort(arr: list[Any]) -> list[Any]:
    if len(arr) <= 1:
        return []
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def bubble_sort(arr: list[Any]) -> None:
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return


def insertion_sort(arr: list[Any]) -> None:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return


def native_sort(arr: list[Any]) -> None:
    arr.sort()
