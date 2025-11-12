import time
n = 20

def fib(n):
    if 1 >= n:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

t0 = time.time()
print(fib(n))
print(time.time() - t0)

