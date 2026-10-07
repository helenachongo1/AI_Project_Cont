'''
def kthElement(a, b, k):
    # Ensure a is the smaller array
    if len(a) > len(b):
        return kthElement(b, a, k)

    # Base cases
    if not a:
        return b[k - 1]
    if k == 1:
        return min(a[0], b[0])

    # Choose how many elements to take from each array
    i = min(len(a), k // 2)
    j = k - i

    if a[i - 1] < b[j - 1]:
        # Drop first i elements from a
        return kthElement(a[i:], b, k - i)
    else:
        # Drop first j elements from b
        return kthElement(a, b[j:], k - j)

a=[2,4,6,9]
b=[1,3,7,8,10]
k=5
res=kthElement(a, b, k)
#print(res)
'''

def platforms(arr,dep):
    n = len(arr)
    res = 0
    for i in range(n):
        count = 1
        for j in range(n):
            if i != j:
                if(arr[i]>=arr[j] and dep[j]>arr[i]):
                    count+=1
        res = max(count,res)
    return res

arr = [900, 940, 950, 1100, 1500, 1800]
dep = [910, 1200, 1120, 1130, 1900, 2000]
ress = platforms(arr, dep)
print(ress)

'''
def freq(arr):
    frequency = {}
    for i in arr:
        frequency[i] = frequency.get(i,0)+1
    f = []
    for i in frequency:
        if frequency[i]%2 != 0:
            f.append(i)
    return f

arr = [2,6,8,3,2,4,8,9,9]
res = freq(arr)
print(res)'''