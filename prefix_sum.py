def function_sum_prefix(arr):
    prefix = [0] * len(arr)
    prefix[0] = arr[0]
    for i in range(1,len(arr)):
        prefix[i]= prefix[i-1] + arr[i]
    
    return prefix

def function_sum_sufix(arr):
    n=len(arr)
    sufix = [0]*n
    sufix[n-1]=arr[n-1]
    for i in range(n-2,-1,-1):
        sufix[i]=sufix[i+1] + arr[i]
    return sufix

arr=[1,3,4,5,2,6]
res = function_sum_prefix(arr)
print("Result:", res)

res_1 = function_sum_sufix(arr)
print("Result:", res_1)



