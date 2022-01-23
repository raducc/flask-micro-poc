from flask_caching import Cache

cache = Cache()


def get_fibonacci(n):
    sqrt5 = pow(5, 1 / 2)
    phi = (1 + sqrt5) / 2
    return int((pow(phi, n) - pow(1 - phi, n)) / sqrt5)


@cache.memoize(timeout=60 * 60)
def get_factorial(n):
    if n in {0, 1}:
        return 1

    return n * get_factorial(n - 1)


def get_factorial_iterative(n):
    result = 1
    for i in range(n, 0, -1):
        result *= i

    return result
