cache = {}


def add(a, b):
    if cache.get(f'{a} {b}', None) is None:
        print('heavy calculations')
        cache[f'{a} {b}'] = a + b
    return cache[f'{a} {b}']


add(1, 2)
add(1, 3)
add(1, 2)
add(1, 2)
add(1, 2)
