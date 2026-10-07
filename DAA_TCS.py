'''from collections import Counter
def non_repeating(arr):
    arr1 = Counter(arr)
    
    for key,a in arr1.items():
        if a == 1:
            ans = key
            break
        
    return ans'''

arr = [9, 4, 9, 6, 7, 4]
#print(non_repeating(arr))

def palindrome_string(strg):
    strg = ''.join(strg.split()).lower()

    if strg==strg[::-1]:
        return "Palindrome"
    else:
        return "Not palindrome"

strg = "Madam"
print(palindrome_string(strg))

def anagram(s1,s2):
    if len(s1) != len(s2):
        return False
    
    s1 = sorted(s1)
    s2 = sorted(s2)
    
    if s1 ==s2:
            
        
    
        

