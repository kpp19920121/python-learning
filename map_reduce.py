def fun1(x :int):
    return x*x;

list_1=[1,2,3,4,5]


for temp in map(fun1,list_1):
    print(temp)



for temp in map(lambda x:x*x,list_1):
    print(temp)


def fun_2(n):
    return n % 2==1

list_2=[1, 2, 4, 5, 6, 9, 10, 15]

print(f"filter=>{type(filter(fun_2,list_2))}")



for temp in filter(fun_2,list_2):
    print("filter=>"+str(temp))




for temp  in filter(lambda n:n%2==1,list_2):
    print("filter=>"+str(temp))




print("开始测试排序")

list_3=[4,2,6,18,9]


list_4=[dict(name='柯凡',age="32"),dict(name='柯凡-1',age="30"),dict(name='柯凡-2',age="33")]


for temp in  sorted(list_3):
    print(temp)


for temp in sorted(list_4,key=lambda  tempObj:tempObj['age'],reverse=True):
    print(f"list_4=>{temp}")



print(__name__)







