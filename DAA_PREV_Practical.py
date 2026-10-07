#Q1
import random

def generate_dna(length=25):
    """Generate random DNA sequence of given length."""
    return ''.join(random.choice('ATGC') for _ in range(length))


def find_subsequence_occurrences(text, pattern):
    """Return all starting indices where pattern occurs in text."""
    positions = []
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i+len(pattern)] == pattern:
            positions.append(i)
    return positions

dna = generate_dna(25)
print("DNA:", dna)

# Call the function to find the pattern
pattern = "AGC"
positions = find_subsequence_occurrences(dna, pattern)
print("Pattern found at positions:", positions)

#Q2
import re

def tokenize(s):
    """Split into lowercase words removing punctuation."""
    tokens = [re.sub(r'^\W+|\W+$', '', w).lower() for w in s.split()]
    return [t for t in tokens if t]


def is_word_subsequence(subseq, text):
    """
    Check if subsequence of words appears in order (not necessarily contiguous).
    Returns True/False and list of matched positions.
    """
    i = 0
    pos = []
    for idx, w in enumerate(text):
        if i < len(subseq) and w == subseq[i]:
            pos.append(idx)
            i += 1
    return i == len(subseq), pos

text = "The paper introduces a new sorting algorithm."
query = "a new sorting algorithm"

subseq = tokenize(query)
text_tokens = tokenize(text)

found, positions = is_word_subsequence(subseq, text_tokens)
print("Found?", found)
print("Positions:", positions)

#Q3
def knapsack(values, weights, capacity):
    """0/1 Knapsack returning max value and chosen item indices."""
    n = len(values)
    dp = [[0]*(capacity+1) for _ in range(n+1)]

    for i in range(1, n+1):
        v = values[i-1]
        w = weights[i-1]
        for c in range(capacity+1):
            dp[i][c] = dp[i-1][c]
            if w <= c:
                dp[i][c] = max(dp[i][c], dp[i-1][c-w] + v)

    chosen = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i-1][c]:
            chosen.append(i-1)
            c -= weights[i-1]

    return dp[n][capacity], chosen[::-1]

values = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50

max_value, chosen_items = knapsack(values, weights, capacity)
print("Max value:", max_value)
print("Chosen item indices:", chosen_items)

#Q4
def min_coins_bounded(denoms, qtys, amount):
    """Bounded coin change using DP + binary splitting."""
    items = []
    for coin, qty in zip(denoms, qtys):
        k = 1
        while qty > 0:
            take = min(k, qty)
            items.append((coin*take, take, coin))
            qty -= take
            k *= 2

    INF = 10**9
    dp = [INF] * (amount+1)
    choice = [-1] * (amount+1)
    dp[0] = 0

    for idx, (value, count, coin) in enumerate(items):
        for s in range(amount, value-1, -1):
            if dp[s-value] + count < dp[s]:
                dp[s] = dp[s-value] + count
                choice[s] = idx

    if dp[amount] == INF:
        return None

    # Reconstruct
    result = {d:0 for d in denoms}
    s = amount
    while s > 0:
        idx = choice[s]
        value, count, coin = items[idx]
        result[coin] += count
        s -= value

    return result

denoms = [1, 2, 5, 10]
qtys =   [5, 2, 1, 1]   # availability of each coin
amount = 14

result = min_coins_bounded(denoms, qtys, amount)
print("Coin usage:", result)

#Q5
def max_segments(n, x, y, z):
    """Maximum pieces from length n using cuts x, y, z."""
    dp = [-10**9] * (n+1)
    dp[0] = 0

    for i in range(1, n+1):
        if i-x >= 0: dp[i] = max(dp[i], dp[i-x] + 1)
        if i-y >= 0: dp[i] = max(dp[i], dp[i-y] + 1)
        if i-z >= 0: dp[i] = max(dp[i], dp[i-z] + 1)

    return max(0, dp[n])

n = 5
x, y, z = 5, 3, 2

ans = max_segments(n, x, y, z)
print("Maximum segments:", ans)

#Q6
def find_bridges(n, edges):
    """Return all bridges in an undirected graph."""
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    low = [0]*n
    disc = [-1]*n
    time = 0
    bridges = []

    def dfs(u, parent):
        nonlocal time
        disc[u] = low[u] = time
        time += 1

        for v in graph[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))
            else:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)

    return bridges

n = 5
edges = [(0,1), (1,2), (2,0), (1,3), (3,4)]

br = find_bridges(n, edges)
print("Bridges:", br)

#Q7
import heapq

def dijkstra_all_paths(n, edges, src):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = [float('inf')] * n
    preds = [[] for _ in range(n)]
    dist[src] = 0

    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                preds[v] = [u]
                heapq.heappush(pq, (nd, v))
            elif nd == dist[v]:
                preds[v].append(u)

    return dist, preds

def recover_paths(preds, src, dest):
    """Recover all shortest paths using predecessor lists."""
    paths = []
    stack = [[dest]]

    while stack:
        path = stack.pop()
        node = path[0]
        if node == src:
            paths.append(path[::-1])
        else:
            for p in preds[node]:
                stack.append([p] + path)

    return paths

n = 5
edges = [
    (0,1,2),
    (0,2,1),
    (1,3,3),
    (2,3,1),
    (3,4,2),
    (2,4,5)
]

dist, preds = dijkstra_all_paths(n, edges, src=0)
paths = recover_paths(preds, src=0, dest=4)

print("Distances:", dist)
print("All shortest paths:", paths)


#Q8
def prime_factors(n):
    """Return prime factorization of n as a list."""
    factors = []
    i = 2
    while i*i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1 if i == 2 else 2
    if n > 1:
        factors.append(n)
    return factors

num = 360
factors = prime_factors(num)
print("Prime factors:", factors)

