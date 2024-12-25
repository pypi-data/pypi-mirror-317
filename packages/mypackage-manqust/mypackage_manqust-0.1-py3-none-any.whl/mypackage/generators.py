# Задача 1. Функция-генератор для ряда Фибоначчи
def fibonacci():
    """Генератор для бесконечного ряда Фибоначчи."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Задача 2. Генератор геометрической прогрессии
def geom_progress(b, q):
    """Генератор для бесконечной геометрической прогрессии с начальным значением b и знаменателем q."""
    b_n = b
    while True:
        yield b_n
        b_n *= q

# Задача 3. Генератор обратного отсчёта
def countdown(n):
    """Генератор обратного отсчёта от n до 0."""
    n_1 = n
    while n_1 >= 0:
        yield n_1
        n_1 -= 1

if __name__ == "__main__":
    print("Фибоначчи (первые 10 чисел):")
    fib_gen = fibonacci()
    for i in range(10):
        print(next(fib_gen), end=" ")
    print("\n")

    print("Геометрическая прогрессия (первые 10 чисел):")
    geom_gen = geom_progress(3, 3)
    for i in range(10):
        print(next(geom_gen), end=" ")
    print("\n")

    print("Обратный отсчёт от 10 до 0:")
    for i in countdown(10):
        print(i, end=" ")
    print()