def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def combination(n, k):
    if k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def placing(n, k):
    if k > n:
        return 0
    return factorial(n) // factorial(n - k)

def permutation(n):
    return factorial(n)