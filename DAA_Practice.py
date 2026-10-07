'''
def Bcandles(arr):
    max_v = arr[0]
    res = 0
    n = len(arr)
    for i in range(1,n):
        if arr[i]>max_v:
            max_v=arr[i]
    for i in range(0,n):
        if arr[i]==max_v:
            res+=1           
    return res

arr = [4,3,2,1,4]
print(Bcandles(arr))

def Ctriplets(a,b):
    c0 = 0
    c1 = 0
    for i in range(0,len(a)):
        if a[i]>b[i]:
            c0 += 1
        elif a[i]<b[i]:
            c1 += 1
    return [c0,c1]

a = [20, 67, 89]
b = [32, 67, 9]

print(Ctriplets(a,b))

# Viral advertising
def advertising(n):
    sum = 0 
    m = 5
    for i in range(n):
        r = m//2 
        sum+=r
        m=r*3
    return sum

n = 4
print(advertising(n))'''

'''
from collections import Counter
def merchant(arr):
    a = Counter(arr)
    res = 0
    for i in a.values():
        res += i//2
    return res

arr = [10,10,20,10,20,10,30,10,20]
print(merchant(arr))'''

def assign_runways(flights, arr, dep):
    # Convert times to integers
    arr = [int(t) for t in arr]
    dep = [int(t) for t in dep]

    # Combine and sort by arrival time
    combined = list(zip(flights, arr, dep))
    combined.sort(key=lambda x: x[1])

    runway_end_times = []       # stores when each runway gets free
    assigned = {}               # flight -> runway number

    for f, a, d in combined:
        assigned_runway = None

        # Try to reuse an available runway
        for i in range(len(runway_end_times)):
            if a >= runway_end_times[i]:
                assigned_runway = i
                runway_end_times[i] = d
                break

        # If no runway free → create new runway
        if assigned_runway is None:
            runway_end_times.append(d)
            assigned_runway = len(runway_end_times) - 1

        assigned[f] = assigned_runway + 1   # runway numbers start at 1

    return assigned

    
flights=['A','B','C','D','E']
arr = ['0900','0915','0935','0940','0950']
dep = ['0920','0930','0945','1100','1000']
print(assign_runways(flights, arr, dep))
                