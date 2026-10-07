'''#Power function using iterative method
def power(base,exponent):
    result = 1
    for i in range(exponent):
        result = base * result
    return result

base = 2
exponent = 5
res = power(base, exponent)
print(res)'''

'''
def power(base, exponent):
    if exponent==0:
        return 1
    elif exponent%2==0:
        return power(base,exponent//2)*power(base,exponent//2)
    else:
        return base*power(base,exponent//2)*power(base,exponent//2)
    
base=2
exponent=5
res=power(base, exponent)
print("Result:", res)'''



'''
#Power function using recursive method
def power(base, exponent):
    if exponent == 0:
            return 1
    else:
        return base*power(base,exponent-1)

base=2
exponent=5
res = power(base, exponent)
print(res)'''

'''
# Including both negative and positive exponents
def power(base, exponent):
    if exponent == 0:
            return 1
    elif exponent < 0:
        return (1/base) * power((1/base),(-1)*exponent-1)
    else:
        return base*power(base,exponent-1)

base=2
exponent=-2
res = power(base, exponent)
print(res) '''

'''
# Or
def power(base, exponent):
    if exponent == 0:
            return 1
    else:
        return base*power(base,exponent-1)

base=2
exponent=-2
res = power(base, abs(exponent))
if(exponent < 0):
    res = 1/res
print(res)'''

'''
#Factorial of n
def fact(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return n * fact(n-1)
    
n=4
res = fact(n)
print("Factorial of ",n,":",res)'''

'''
#Sum of n numbers
def sum(n):
    if n == 0:
        return 0
    else:
        return n + sum(n-1)
    
n=10
res=sum(n)
print('Sum is:',res)'''



