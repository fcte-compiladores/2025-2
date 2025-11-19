import time

def make_fib():
    def fib(n):
        if 1 >= n:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)
    return fib

f = make_fib()
t0 = time.time()
for _ in range(1000):
    f(20)
print(time.time() - t0)

