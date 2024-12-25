def factorial(n):
    f = 1
    for i in range(1, n + 1):
        f *= i
    return f


def permutation(n):
    return factorial(n)


def compination(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))

def binkof(n,k):
    return factorial(n)/(factorial(k)*factorial(n-k))

def gamma(n):
    return factorial(n-1)

def summaf(n):
    h=0
    for i in range(n+1):
        if i!=0:
            h+=factorial(i)
    return h
