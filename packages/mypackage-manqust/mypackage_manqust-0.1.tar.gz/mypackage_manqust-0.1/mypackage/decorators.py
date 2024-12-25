# Декоратор со скобками и без
import time
from functools import wraps

def timeit(func=None, *, min_seconds=0):
    if func and callable(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            print(f"Функция '{func.__name__}' выполнена за {elapsed_time:.6f} секунд")
            return result
        return wrapper

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = f(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            if elapsed_time > min_seconds:
                print(f"Функция '{f.__name__}' выполнена за {elapsed_time:.6f} секунд")
            return result
        return wrapper

    return decorator

if __name__ == "__main__":
    @timeit
    def slow_sum(a, b, *, delay):
        time.sleep(delay)
        return a + b

    @timeit(min_seconds=2)
    def slow_mul(a, b, *, delay):
        time.sleep(delay)
        return a * b

    print(slow_sum(1, 2, delay=1))
    print(slow_mul(3, 3, delay=1))