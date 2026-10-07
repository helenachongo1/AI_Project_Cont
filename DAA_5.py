'''
#Min-Max
def minmax(arr):
    if len(arr)==1:
        return (arr[0],arr[0])
    mid = len(arr)//2
    lmin,lmax = minmax(arr[:mid])
    rmin,rmax=minmax(arr[mid:])
    
    return (min(lmin,rmin),max(lmax,rmax))

arr=[2,4,5,7,1,9]
res=minmax(arr)
print(res)

'''

