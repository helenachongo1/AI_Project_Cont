'''#Linear search
def linear_search (arr,key):
    for i in range (0,len(arr)):
        if(key==arr[i]):
            print("Element found")
            return
        print("Element not found")
        
        
arr=[1,3,5,4,7,8,9]
key=1
linear_search(arr, key)'''

#Write code for counting occcurence of key
#Identify the number of times a key is occuring in odd indices

def linear_search(arr,key):
    for i in range(len(arr)):
        if key == arr[i]:
            print("Element found at index", i)
            return
    print("Element not found")

arr=[1,3,5,4,7,8,9]
key=1
linear_search(arr, key)

'''
#Selection sort
def selection_sort(arr):
    for i in range(0,len(arr)):
        min_index=i
        for j in range(i+1, len(arr)):
            if (arr[min_index]>arr[j]):
                min_index=j
                
                arr[i], arr[min_index]=arr[min_index],arr[i]
    return arr
                
                
arr=[1, 5, 3, 2, 8, 9]
selection_sort(arr)
print(arr)'''

