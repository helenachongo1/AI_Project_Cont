def naive_string_match(text, pattern):
    n = len(text)
    m = len(pattern)
    positions = []  # store all match indices

    # Slide pattern over text
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            positions.append(i)

    return positions


text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
result = naive_string_match(text, pattern)

print("Pattern found at indices:", result)

'''
https://leetcode.com/problems/string-matching-in-an-array/description/

https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/?envType=problem-list-v2&envId=string-matching& 

https://leetcode.com/problems/substring-matching-pattern/description/

'''