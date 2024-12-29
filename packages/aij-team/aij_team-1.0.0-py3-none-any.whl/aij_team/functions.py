def add(num1:int,num2:int):
    return num1 + num2

def subtract(num1:int, num2:int):
    return num1 - num2

def multiply(num1:int, num2:int):
    return num1 * num2

def divide(num1:int, num2:int):
    if num2 == 0:
        raise ValueError("Cannot divide by zero")
    return num1 / num2

def power(base: int, exponent: int):
    return base ** exponent

def factorial(num: int):
    if num < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(1, num + 1):
        result *= i
    return result

def fibonacci(n: int):
    if n < 0:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    if n <= 2:
        return [1] * n
    fib_sequence = [1, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence

def is_prime(num: int):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def is_palindrome(s: str):
    s = s.lower()
    return s == s[::-1]

def reverse_string(s: str):
    return s[::-1]

def find_common_elements(list1: list, list2: list):
    return list(set(list1) & set(list2))

def find_unique_elements(list1: list, list2: list):
    return list(set(list1) ^ set(list2))

def merge_sorted_lists(list1: list, list2: list):
    merged_list = list1 + list2
    merged_list.sort()
    return merged_list

def find_max_element(list1: list):

    return max(list1)

def find_min_element(list1: list):
    return min(list1)

def find_average(list1: list):
    return sum(list1) / len(list1)

    