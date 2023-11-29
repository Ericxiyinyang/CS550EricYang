memo = {}

def fibonacci(n):
    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fibonacci(n - 1) + fibonacci(n - 2)
    return memo[n]


for i in range(10000):
    print(fibonacci(i), end=" ")
