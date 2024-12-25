# Задача 1. Итератор, который проходит по числам начиная с 10 и до указанного предела
def range_iterator(limit):
    return iter(range(10, limit + 1))


# Задача 2. Бесконечный итератор
import itertools

# (A) – Числа, кратные 7 и 9
def multiples_of_7_and_9(limit):
    for i in range(limit):
        if i % 7 == 0 and i % 9 == 0:
            yield i

# (B) – Повторить строки 15 раз
def repeat_string_15_times(string):
    return itertools.repeat(string, 15)

# (C) – Повторить значение 38 раз
def repeat_value_38_times(value):
    return itertools.repeat(value, 38)


# Задача 3. Итератор для перестановок и комбинаций

# (A) – Все возможные перестановки списка
def permutations(lst):
    if len(lst) <= 1:
        yield lst
    else:
        for i in range(len(lst)):
            el = lst[i]
            lst_wotel = lst[:i] + lst[i + 1:]
            for p in permutations(lst_wotel):
                yield [el] + p

# (B) – Все возможные комбинации в списке без замены в отсортированном порядке
def combinations(lst, d):
    if d == 0:
        yield []
    elif len(lst) < d:
        return
    else:
        for comb in combinations(lst[1:], d - 1):
            yield [lst[0]] + comb
        for comb in combinations(lst[1:], d):
            yield comb


# Задача 4. Итератор для преобразования фраз
def transform_phrases(phrases):
    for phrase in phrases:
        words = [word for word in phrase.split() if word.lower() != 'of']
        transformed_words = [word[:-1] if word.endswith('s') and len(word) > 1 else word for word in words]
        yield ' '.join(transformed_words)

if __name__ == "__main__":
    print("Числа от 10 до 15:")
    for num in range_iterator(15):
        print(num, end=" ")
    print("\n")

    print("Числа, кратные 7 и 9 до 500:")
    for num in multiples_of_7_and_9(500):
        print(num, end=" ")
    print("\n")

    print("Повтор строки 'OOO' 15 раз:")
    for string in repeat_string_15_times("OOO"):
        print(string)
    print("\n")

    print("Повтор значения 23 38 раз:")
    for value in repeat_value_38_times(23):
        print(value)
    print("\n")

    print("Перестновки массива [1, 2, 3]:")
    for lst in permutations([1, 2, 3]):
        print(lst)
    print("\n")

    print("Комбинации в списке без замены в отсортированном порядке, список - [1, 2, 3], длина - 2:")
    for lst in combinations([1, 2, 3], 2):
        print(lst)
    print("\n")

    print("Итератор для преобразования фраз, фразы - basket Of apples, Group oF dogs, collection OF books, list of tasks:")
    phrases = [
        "basket Of apples",
        "Group oF dogs",
        "collection OF books",
        "list of tasks"
    ]
    for phrase in transform_phrases(phrases):
        print(phrase)
    print("\n")