#Iterative approach for Fibonacci
def fib(n):
    f = [-1]*(n+1) #f[=[-1 for i in range(n+1)]
    f[0]=0
    f[1]=1
    for i in range(2,n+1):
        f[i]=f[i-1]+f[i-2]
    
    return f[n]

#Recursive approach
def fibonacci(n):
    if n < 0:
        return -1
    if n <= 1:
        return n
    
    return fibonacci(n-1)+fibonacci(n-2)

n=8
res = fib(n)
print("Result:", res)
res_1 = fibonacci(n)
print("Result:", res_1)

#Longest subsequence 

