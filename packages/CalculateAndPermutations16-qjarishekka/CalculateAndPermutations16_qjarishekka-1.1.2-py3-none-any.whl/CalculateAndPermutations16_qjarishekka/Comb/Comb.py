def factorial(n):
    f = 1
    for i in range(1,n+1):
        f *= i
    return f


def permutation(n):
    return factorial(n)

def combination(n ,k):
    return factorial(n)/ (factorial(k) * factorial(n-k))
