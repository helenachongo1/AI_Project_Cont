#Linear search as time complexity of O(n) and space complexity of O(1)
#Selection sort as time complexity of O(n^2) and space complexity of O(1)

#In Insertion sort, we rearrenge the array, by shifting the key to left side till we find the elemnt less than the key

'''
#Insertion sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j=i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j-=1
        arr[j+1] = key

arr=[1,4,2,1,6,4,2,7,3,4]
insertion_sort(arr)
print(arr)'''

'''
#Counting sort
arr=[1,4,2,1,6,4,2,7,3,4]
max_number = arr[0]
for i in range(len(arr)):
    if(arr[i]>max_number):
        max_number=arr[i]
        
count =[0 for i in range(max_number+1)]
for i in range(len(arr)):
    count[arr[i]]=count[arr[i]]+1 
    
for i in range(len(count)):
    for j in range(count[i]):
        print(i)  '''
        

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

arr=[1,4,2,1,6,4,2,7,3,4]
arr_sorted = bubble_sort(arr)
print("Sorted array:", arr_sorted)


    
# Homework    
#Sort the characters (alphabets and digits) using counting sort
#ord('A') - to find the ASCII value
#chr(65) - to find the respective character 