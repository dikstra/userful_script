import itertools
from functools import lru_cache

def fibo(num):
    fibo_list = []
    if num <= 0:
        return fibo_list
    else:
        x, y = 0, 1
        for i in range(num):
            fibo_list.append(y)
            x,y = y ,x+y
        return fibo_list

#a=fibo(10)
#print(a)
def fibo_genetator():
    x, y = 0, 1
    while True:
        yield y
        x, y = y, x + y

#print(list(itertools.islice(fibo_genetator(), 10)))

@lru_cache(maxsize=None)
def fibo_recursive(num):
    if num < 0:
        return 0
    if num <= 1:
        return num
    return fibo_recursive(num - 1) + fibo_recursive(num - 2)

print([fibo_recursive(i) for i in range(1, 11)])
