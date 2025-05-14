

def cal(*args):
    sum=0
    for n in args:
        sum+=n;
    return sum




def cal2(**kwargs):
    print(type(kwargs))
    for key,value in kwargs.items():
        print("key->"+key+"value->"+value)



sum=cal(1,2,3)
print(sum)





cal2(name='张伟',age='15')

