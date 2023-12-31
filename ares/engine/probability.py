

from random import randint


def die(num: int, size: int = 20):
    def pool():
        for _ in range(num):
            yield randint(1, size)
    return pool

def best_of(pool: list[int], amount: int):
    pool_size = len(pool)
    if amount > pool_size:
        amount = pool_size
    start_from = pool_size - amount
    return sorted(pool)[start_from:]

