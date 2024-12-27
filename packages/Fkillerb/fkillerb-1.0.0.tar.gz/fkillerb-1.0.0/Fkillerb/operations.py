import math
def exp(b, e):
    return b**e
def log(b,e):
    return math.log(b,e)
def fac(b):
    ans=1
    for i in range(b):
        ans=ans*(i+1)
    return ans
def mul(cs):##乘法
    ans=1
    if cs <= 0:
        return ans
    for i in range(cs):
        k=float(input("请输入数字"))
        ans*=k
    return ans
def div(b,c):##除法
    ans=b
    if c <= 0:
        return ans
    for i in range(c):
        k=float(input("请输入数字"))
        while k==0:
            print("重新输入")
            k = float(input("请输入数字"))
        ans/=k
    return ans
def add(cs):
    ans=0
    if cs<=0:
        return ans
    for i in range(cs):
        k=float(input("请输入数字"))
        ans+=k
    return ans
def sub(b,c):
    ans=b
    if c <= 0:
        return ans
    for i in range(c):
        k=float(input("请输入数字"))
        ans-=k
    return ans
