import functools
import sys


def decorator(fun):

    @functools.wraps(fun)
    def wrapper(*args):
        print("==========准备调用函数===========")
        fun(args)
        print("1=>"+__name__)
        print("==========结束调用函数===========")
    return wrapper
@decorator
def fun_1(name):

    print(f"say hello {name}")

#decorator(fun_1)('柯凡')


fun_1('柯凡')
print(fun_1.__name__)



for temp in sys.path:
    print(temp)