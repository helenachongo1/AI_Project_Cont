# 1 Compare triplets
def compare_triplets(a, b):
    # Input validation
    if not (isinstance(a, list) and isinstance(b, list)):
        raise TypeError("Inputs must be lists.")
    if len(a) != 3 or len(b) != 3:
        raise ValueError("Each list must contain exactly 3 integers.")
    if not all(isinstance(x, int) for x in a + b):
        raise TypeError("All elements must be integers.")

    alice_score = 0
    bob_score = 0

    # Compare each category
    for alice_val, bob_val in zip(a, b):
        if alice_val > bob_val:
            alice_score += 1
        elif bob_val > alice_val:
            bob_score += 1
        # If equal, no points awarded

    return [alice_score, bob_score]

# 2 Avery big sum
def a_very_big_sum(numbers):
    if not all(isinstance(x, int) for x in numbers):
        raise ValueError("All elements must be integers.")
    return sum(numbers)

# 3 Diagonal difference
def diagonalDifference(arr):
    n = len(arr)
    d1 = sum([arr[i][i] for i in range(n)])
    d2 = sum([arr[i][n - i - 1] for i in range(n)])
    return abs(d1 - d2)

# 4 Beatiful days at the movies
def beautifulDays(i, j, k):
    return sum(abs(x - int(str(x)[::-1])) % k == 0 for x in range(i, j + 1))

# 5 Between two sets
def getTotalX(a, b):
    res = 0
    for i in range(max(a), min(b) + 1):
        res += (all([i % aa == 0 for aa in a]) and all([bb % i == 0 for bb in b]))
    return res

# 6 Birthday cake candles
def birthdayCakeCandles(candles):
    m = 0
    res = 0
    for c in candles:
        if c > m:
            m = c
            res = 1
        elif c == m:
            res += 1
    return res

# 7 Bon appetit
def bonAppetit(bill, k, b):
    x = (sum(bill[:k]) + sum(bill[k+1:])) // 2
    if b == x:
        print("Bon Appetit")
    else:
        print(b - x)

# 8 Breaking best and worst records
def breakingRecords(scores):
    high, highs, low, lows = scores[0], 0, scores[0], 0
    for s in scores:
        if s > high:
            high = s
            highs += 1
        elif s < low:
            low = s
            lows += 1
    return highs, lows

# 9 Cats and a mouse
def catAndMouse(x, y, z):
    dx = abs(z - x)
    dy = abs(z - y)
    if dx < dy:
        return "Cat A"
    elif dx > dy:
        return "Cat B"
    else:
        return "Mouse C"

# 10 Circular array rotaion
def circularArrayRotation(a, k, queries):
    x = k % len(a)
    a = a[-x:] + a[:-x]
    res = []
    for q in queries:
        res.append(a[q])
    return res

# 11 Climbing the leaderboard
def climbingLeaderboard(ranked, player):
    res = []
    x = [(ranked[0], 1)]
    for r in ranked[1:]:
        if r != x[-1][0]:
            x.append((r, x[-1][1] + 1))
    i = len(x) - 1
    for p in player:
        while i >= 0 and p > x[i][0]:
            i -= 1
        if i < 0:
            res.append(1)
        elif p == x[i][0]:
            res.append(x[i][1])
        else:
            res.append(x[i][1] + 1)
    return res

# 12 Counting valleys
def countingValleys(steps, path):
    valleys = 0
    level = 0
    for step in path:
        level += 1 if step == "U" else -1
        if level == 0 and step == "U":
            valleys += 1
    return valleys

# 13 Cut the sticks
def cutTheSticks(arr):
    d = defaultdict(int)
    for a in arr:
        d[a] += 1
    d = sorted(list(d.items()))
    res = [len(arr)]
    for _, n in d[:-1]:
        res.append(res[-1] - n)
    return res

# 14 Day of the programmer
def dayOfProgrammer(year):
    if year <= 1917:
        return f"{12 if year % 4 == 0 else 13}.09.{year}"
    elif year == 1918:
        return "26.09.1918"
    else:
        d = 12 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 13
        return f"{d}.09.{year}"

# 15 Divisible sum pairs
def divisibleSumPairs(n, k, ar):
    res = 0
    for i in range(n):
        for j in range(i + 1, n):
            res += ((ar[i] + ar[j]) % k == 0)
    return res

# 16 Electronic shop
def getMoneySpent(keyboards, drives, b):
    keyboards.sort()
    drives.sort()
    res = -1
    for k in keyboards:
        x = -1
        for d in drives:
            if k + d <= b:
                x = k + d
            else:
                break
        if x == -1:
            break
        else:
            res = max(res, x)
    return res

# 17 Finf digits
def findDigits(n):
    return sum(n % int(c) == 0 for c in str(n) if c != "0")

# 18 Extra long factorial
def extraLongFactorials(n):
    f = lambda x: x * f(x - 1) if x > 1 else 1
    print(f(n))

# 19 Grading
def gradingStudents(grades):
    return [g if g <= 37 or g % 5 <= 2 else g + 5 - (g % 5) for g in grades]

# 20 Jumping on the clouds revisited
def jumpingOnClouds(c, k):
    e = 100
    i = 0
    while True:
        i = (i + k) % len(c)
        e -= 1 + (2 * c[i])
        if i == 0:
            break
    return e


def theLoveLetterMystery(s):
    ret = 0
    n = len(s)

    for i in range(n // 2):
        ret += abs(ord(s[i]) - ord(s[n-1-i]))

    return ret


def maximumToys(prices, k):
    result = 0
    price = 0
    prices.sort()

    while price < k:
        for p in prices:
            if price + p < k:
                result += 1
                price += p
            else:
                return result

    return result


import collections
def isValid(s):
    c = collections.Counter(s)
    c = list(c.values())
    c.sort()
    r = 'YES' if c.count(c[0]) == len(c) or (c.count(c[0]) == len(c) - 1 and c[-1] - c[-2] == 1) or (c.count(c[-1]) == len(c) - 1 and c[0] == 1) else 'NO'
    return r

# Quicksort
def quickSort(arr):
    pivot = arr[0]
    left, right = [], []

    for i in arr[1:]:
        if i <pivot:
            left.append(i)
        else:
            right.append(i)

    return left + [pivot] + right

# Correctness and the loop invariant
def insertion_sort(l):
    for i in range(1, len(l)):
        j = i-1
        key = l[i]
        while (j >= 0) and (l[j] > key):
           l[j+1] = l[j]
           j -= 1
        l[j+1] = key

m = int(input().strip())
ar = [int(i) for i in input().strip().split()]
insertion_sort(ar)
print(" ".join(map(str,ar)))

# Running time of algorithms
def runningTime(arr):
    ret = 0
    for i in range(1, n):
        tmp = arr[i]
        j = i-1

        while j >= 0 and arr[j] > tmp:
            arr[j+1] = arr[j]
            j -= 1
            ret += 1

        arr[j+1] = tmp

    return ret

#Counting sort 2
def countingSort(arr):
    s = [0 for _ in range(100)]
    ret = []

    for i in arr:
        s[i] += 1

    for i in range(len(s)):
        for j in range(s[i]):
            ret.append(i)

    return ret

#Counting sort 1
def countingSort(arr):
    ret = [0 for _ in range(100)]

    for i in arr:
        ret[i] += 1

    return ret

#Happy ladybugs
from collections import Counter
def happyLadybugs(b):
    c = Counter(b)

    for a in set(b):
        if a != "_" and c[a] == 1:
            return "NO"

    if c["_"] == 0:
        for i in range(1, n-1):
            if b[i-1] != b[i] and b[i+1] != b[i]:
                return "NO"

    return "YES"

#Cavity map
def cavityMap(grid):
    change = []

    for i in range(1, len(grid)-1):
        for j in range(1, len(grid)-1):
            if grid[i][j] > grid[i-1][j] and grid[i][j] > grid[i+1][j] and grid[i][j] > grid[i][j-1] and grid[i][j] > grid[i][j+1]:
                change.append([i, j]);

    grid = [list(i) for i in grid]

    for c in change:
        grid[c[0]][c[1]] = 'X'

    grid = [''.join(i) for i in grid]

    return grid

# Service lane
def serviceLane(n, cases, width):
    ret = []

    for case in cases:
        w = width[case[0]:case[1]+1]
        m = min(w)
        if w[0] >= m and w[-1] >= m:
            ret.append(m)

    return ret


