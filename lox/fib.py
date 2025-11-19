import time

def fib(n):
    if 1 >= n:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

t0 = time.time()
for i in range(1000):
    fib(20)
print(time.time() - t0)

