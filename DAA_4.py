'''
def power(x,n):
    if n==0:
        return 1
    temp = power(x, n//2)
    if n%2 == 0:
        return temp * temp
    else:
        return x* temp * temp

x = 2
n = -5
res = power(x, abs(n))
if(n < 0):
    res = 1/res
print(res)'''


'''
def binarysearch(arr,l,r,key):
    if l<=r:
        mid = (l+r)//2
        if(arr[mid]==key):
            return mid
        elif (arr[mid]<key):
            return binarysearch(arr, mid+1, r, key)
        else:
            return binarysearch(arr, l, mid-1, key)
    else:
        return -1
    
arr = [1,2,4,5,6,7,9,11,14]
key = 1
l = 0
r = len(arr)-1
print(binarysearch(arr, l, r, key))'''
        
